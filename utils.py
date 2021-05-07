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


class VTRequests:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = vt.Client(self.api_key)

    def url_scanner(self, url: str):
        analysis = self.client.scan_url(url, wait_for_completion=True)
        return analysis.status

    def get_analysis(self, url: str):
        url_id = vt.url_id(url)
        url_analysis = self.client.get_object("/urls/{}", url_id)
        return url_analysis.last_analysis_stats

    def close_client(self) -> bool:
        self.client.close()
        return True


if __name__ == '__main__':
    client = vt.Client(API_KEY)
    site = "www.wordpress.org"
    # analysis = client.scan_url(site, wait_for_completion=True)
    # print(analysis.status)

    url_id = vt.url_id(site)
    url = client.get_object("/urls/{}", url_id)
    print(url.last_analysis_stats)
    print(type(url.last_analysis_stats))
    # analysis = client.scan_url("www.elementor.com")
    client.close()
