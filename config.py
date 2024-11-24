import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="./config/.env", override=True)

ID_TABLE = os.environ.get("ID_TABLE")
NAME_SPREADSHEET = os.environ.get("SPREADSHEET")
