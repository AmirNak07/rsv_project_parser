import time

import gspread
import httpx
import schedule
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials

from config import ID_TABLE, LOGS_CONFIG, NAME_SPREADSHEET
from utils import clean_href, create_table, get_href, write_to_table


logger.remove()
logger.configure(**LOGS_CONFIG)


@logger.catch
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

    logger.info("Начало парсинга")

    request = httpx.get(link + "competitions/", params=params)
    if request.status_code == 200:
        request = request.content
    else:
        request.raise_for_status()

    projects = create_table(get_href(clean_href(request), link))
    table = [["Название", "Описание", "Cсылка", "Для кого", "Возможности"]]
    if projects is not None:
        table = [["Название", "Описание", "Cсылка", "Для кого", "Возможности"]] + projects
    write_to_table(client, id_table, name_worksheet, table)
    logger.info("Парсинг прошёл успешно")


if __name__ == "__main__":
    schedule.every(3).hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # main()
