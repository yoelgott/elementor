import pandas as pd
import datetime as dt

from utils import SqlLiteConnection, VTAssessment
from config import *


class Main:
    def __init__(self):
        self.sql_conn = SqlLiteConnection(DB_FILE_PATH)
        self.vt_assessment = VTAssessment(API_KEY)

    def run(self):
        sites_df = self.get_sites()
        sites_df = self.check_for_risks(sites_df)
        self.vt_assessment.close_client()

        self.sql_conn.dump_to_db(sites_df, TABLE_NAME)
        print("hello")

    def check_for_risks(self, sites_df: pd.DataFrame) -> pd.DataFrame:
        sites_df[[TableCols.RISK.value, TableCols.ANALYSIS_TIME.value]] = sites_df[[TableCols.SITE.value]].apply(
            self._vt_handler, axis=1, result_type="expand")
        return sites_df

    def _vt_handler(self, site: str):
        print(site)
        if self._is_old_analysis(site):
            status = self.vt_assessment.site_scanner(site)
            print(status)
            analysis_time = dt.datetime.now()
            analysis = self.vt_assessment.get_analysis(site)
            return analysis, analysis_time
        return None, None

    def _is_old_analysis(self, site: str) -> bool:
        return False

    @staticmethod
    def get_sites() -> pd.DataFrame:
        df: pd.DataFrame = pd.read_csv(CSV_SITES_URL, header=None)
        col_name = TableCols.SITE.value
        df.columns = [col_name]
        return df


if __name__ == '__main__':
    main_obj = Main()
    main_obj.run()
