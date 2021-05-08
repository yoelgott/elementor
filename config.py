from enum import Enum

DB_FILE_PATH = "db/elementor.db"

CSV_SITES = "sites/sites.csv"

API_KEY = "2705c35dc2cf9814555afc697843696bebd3902a5f343db6d20293cae7f48534"

SITE_RISKS = ["malware", "malicious", "phishing"]

OLD_SCAN_TIME_DELTA = 0.5  # in hours

RISKS_TABLE_NAME = "sites_risk"
class RisksTableCols(Enum):
    """
    table column names for '' table.
    the order of column here will setermine the order of the column names in the table
    """
    SITE = "site"
    RISK = "risk"
    INSERTION_TIME = "insertion_time"


VOTING_TABLE_NAME = "sites_votings"
class VotingTableCols(Enum):
    """
    table column names for '' table.
    the order of column here will setermine the order of the column names in the table
    """
    SITE = "site"
    VOTE = "vote"
    COUNT = "count"
    INSERTION_TIME = "insertion_time"
