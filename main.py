import gspread
import httpx
from oauth2client.service_account import ServiceAccountCredentials

from utils import clean_href, create_table, get_href, write_to_table
from config import ID_TABLE, NAME_SPREADSHEET


def main():
    id_table = ID_TABLE
    name_worksheet = NAME_SPREADSHEET

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "config/credentials.json", scope)
    client = gspread.authorize(creds)

    link = "https://rsv.ru/"
    params = {"registration": "true"}

    request = httpx.get(link + "competitions/", params=params)
    if request.status_code == 200:
        request = request.content
    else:
        request.raise_for_status()

    projects = create_table(get_href(clean_href(request), link))
    projects = [["Название", "Описание", "Cсылка", "Для кого", "Возможности"]] + projects
    write_to_table(client, id_table, name_worksheet, projects)


if __name__ == "__main__":
    main()
