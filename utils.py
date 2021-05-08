import pandas as pd
import sqlite3
import datetime as dt
from virus_total_apis import PublicApi as VirusTotalPublicApi

from config import *


class SqlLiteConnection:
    def __init__(self, db_file="db/elementor.db"):
        self.conn = self._connect_to_db(db_file)

    @staticmethod
    def _connect_to_db(db_file: str):
        """ create a database connection to a SQLite database """
        conn = sqlite3.connect(db_file)
        return conn

    def dump_to_db(self, df: pd.DataFrame, table_name: str, if_exists="append"):
        """
        insert a Dataframe to db
        :param df: Dataframe to insert
        :param table_name: witch table to insert to
        :param if_exists: in case the table already exists how to insert the Dataframe
        """
        df.to_sql(table_name, self.conn, index=False, if_exists=if_exists)

    def query_db(self, query: str) -> pd.DataFrame:
        """
        :param query:
        :return: Dataframe with query results
        """
        df = pd.read_sql(query, self.conn)
        return df

    def close_connection(self):
        """ close connection with db """
        self.conn.close()

    def get_connection(self):
        """ get the connection object """
        return self.conn


class VTAssessment:
    def __init__(self, site, client=None, api_key=None):
        self.site = site

        if not client and not api_key:
            self.client = VirusTotalPublicApi(api_key)
        elif not client:
            raise Exception("either client object or API-KEY was not provided")
        else:
            self.client = client

        self.response = None

        self.site_risk_results = pd.Series()

    def site_scanner(self, scan="1"):
        response = self.client.get_url_report(this_url=self.site, scan=scan)
        self.response = response
        return response

    def is_risk(self) -> bool:
        if len(self.site_risk_results) == 0:
            self._extract_site_risks()

        risks_num = self.site_risk_results.isin(SITE_RISKS).sum()
        return risks_num > 1

    def voting_categories(self):
        if len(self.site_risk_results) == 0:
            self._extract_site_risks()
        return self.site_risk_results.value_counts()

    def _extract_site_risks(self):
        scans = self.response["results"]["scans"]
        risks = [res["result"].replace("site", "").strip() for res in scans.values()]
        self.site_risk_results = pd.Series(risks)

    def is_old_data(self) -> bool:
        scan_time_str = self.response["results"]["scan_date"]
        scan_time = dt.datetime.strptime(scan_time_str, "%Y-%m-%d %H:%M:%S")
        return dt.datetime.now() - dt.timedelta(hours=0.5) > scan_time


if __name__ == '__main__':
    conn = SqlLiteConnection(DB_FILE_PATH)

    query = """
        select *
        from sites_risk
    """

    df = conn.query_db(query)
    conn.close_connection()
    print(df)
