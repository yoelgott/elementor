import pandas as pd

from utils import SqlLiteConnection
from config import *


class Main:
    def __init__(self):
        self.sql_conn = SqlLiteConnection(DB_FILE_PATH)

    def run(self):
        sites_df = self.get_sites()

        print("hello")

    @staticmethod
    def get_sites() -> pd.DataFrame:
        df = pd.read_csv(CSV_SITES_URL)
        return df


if __name__ == '__main__':
    main_obj = Main()
    main_obj.run()
