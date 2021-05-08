import pandas as pd
import sqlite3
import vt

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
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = vt.Client(self.api_key)

    def site_scanner(self, site: str):
        analysis = self.client.scan_url(site, wait_for_completion=True)
        return analysis.status

    def get_analysis(self, site: str):
        site_id = vt.url_id(site)
        site_analysis = self.client.get_object(f"/sites/{site_id}")
        return site_analysis.last_analysis_stats

    def close_client(self) -> bool:
        self.client.close()
        return True


if __name__ == '__main__':
    conn = SqlLiteConnection(DB_FILE_PATH)

    query = """
        select *
        from sites_risk
    """

    df = conn.query_db(query)
    conn.close_connection()
    print(df)
