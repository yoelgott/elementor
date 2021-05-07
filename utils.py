import pandas as pd
import sqlite3


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


if __name__ == '__main__':
    SqlLiteConnection()
