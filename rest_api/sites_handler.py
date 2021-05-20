import pandas as pd
import datetime as dt
from virus_total_apis import PublicApi as VirusTotalPublicApi
import sys
sys.path.append("../")

from elementor.utils import SqlLiteConnection, VTAssessment
from elementor.config import *


class SitesHandler:
    def __init__(self, sites):
        self.sql_conn = SqlLiteConnection(DB_FILE_PATH)
        self.vt_client = VirusTotalPublicApi(API_KEY)

        self.sites = sites

        self.risks_df = pd.DataFrame()
        self.votings_df = pd.DataFrame()

    def run(self):
        print("Started Assessing sites at: ", dt.datetime.now())
        sites_df = self.set_sites()
        self.assessing(sites_df)
        self.handle_dfs()
        self.load_to_db()
        return_data = self.parse_return_data()
        print("Finished Assessing sites at: ", dt.datetime.now())
        return return_data

    def parse_return_data(self):
        return_data = self.risks_df[[RisksTableCols.SITE.value, RisksTableCols.RISK.value]].to_dict(orient="records")
        return return_data

    def load_to_db(self):
        self.sql_conn.dump_to_db(self.risks_df, RISKS_TABLE_NAME, if_exists="replace")
        self.sql_conn.dump_to_db(self.votings_df, VOTING_TABLE_NAME, if_exists="replace")

    def handle_dfs(self):
        self.risks_df[RisksTableCols.INSERTION_TIME.value] = dt.datetime.now()
        self.votings_df[VotingTableCols.INSERTION_TIME.value] = dt.datetime.now()

        self.risks_df = self.risks_df[[col.value for col in RisksTableCols]]
        self.votings_df = self.votings_df[[col.value for col in VotingTableCols]]

    def assessing(self, sites_df):
        for site in sites_df[RisksTableCols.SITE.value]:
            vt_asses = VTAssessment(site, self.vt_client)
            response = vt_asses.site_scanner(scan="0")

            # this part of code is only because i'm using the public api and i dont want to wait a whole minute for the response..
            if response["response_code"] != 200:
                return None

            if vt_asses.is_old_data():
                response = vt_asses.site_scanner(scan="1")

                # this part of code is only because i'm using the public api and i dont want to wait a whole minute for the response..
                if response["response_code"] != 200:
                    return None

                vt_asses = self.risks_assess(site, vt_asses)
                vt_asses = self.voting_assess(site, vt_asses)

    def risks_assess(self, site, vt_asses):
        if vt_asses.is_risk():
            assessment = "risk"
        else:
            assessment = "safe"
        assess_data = {RisksTableCols.SITE.value: site, RisksTableCols.RISK.value: assessment}
        risks = pd.DataFrame([assess_data])
        self.risks_df = pd.concat([self.risks_df, risks], ignore_index=True)
        return vt_asses

    def voting_assess(self, site, vt_asses):
        votings: pd.Series = vt_asses.voting_categories()
        votings = votings.reset_index()
        votings.columns = [VotingTableCols.VOTE.value, VotingTableCols.COUNT.value]
        votings[VotingTableCols.SITE.value] = site
        self.votings_df = pd.concat([self.votings_df, votings], ignore_index=True)
        return vt_asses

    def set_sites(self) -> pd.DataFrame:
        col_name = RisksTableCols.SITE.value
        df = pd.DataFrame({col_name: self.sites})
        df[col_name] = df[col_name].str.strip()
        df = df.drop_duplicates()
        return df
