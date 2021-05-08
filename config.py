from enum import Enum

DB_FILE_PATH = "db/elementor.db"

CSV_SITES_URL = "https://elementor-pub.s3.eu-central-1.amazonaws.com/Data-Enginner/Challenge1/request1.csv"

API_KEY = "2705c35dc2cf9814555afc697843696bebd3902a5f343db6d20293cae7f48534"
TABLE_NAME = "sites_risk"


class TableCols(Enum):
    """
    table column names for '' table.
    the order of column here will setermine the order of the column names in the table
    """
    SITE = "site"
    RISK = "risk"
    ANALYSIS_TIME = "analysis_time"
