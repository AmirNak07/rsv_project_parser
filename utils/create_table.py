import httpx
from bs4 import BeautifulSoup
from loguru import logger


@logger.catch
def create_table(projects_href: list) -> list:
    result = []

    for project in projects_href:
        temp = []
        html = httpx.get(project[0], params=project[1]).content
        soup = BeautifulSoup(html, "html.parser")
        # Название
        temp.append(soup.find("h3", class_="project-detail-block__title").text)
        # Описание с картинки
        temp.append(soup.find("span", class_="detail-image__badge-target_audience").text.strip())
        # Ссылка
        temp.append(project[0])

        # Возможности, для кого
        blocks = soup.find_all("div", class_="block-narrow")
        scope, audience = "-", "-"
        for block in blocks:
            try:
                block_title = block.find("div", class_="block-narrow__title").text
            except AttributeError:
                continue
            if block_title == "Возможности":
                scope = list(map(lambda x: x.text.replace("\xa0", ""), block.find_all("a", class_="block-narrow__link")))
            if block_title == "Для кого":
                audience = list(map(lambda x: x.text.replace("\xa0", ""), block.find_all("a", class_="block-narrow__link")))

        scope = ", ".join(map(lambda x: x.lower(), scope))
        scope = scope[0].upper() + scope[1:]

        audience = ", ".join(map(lambda x: x.lower(), audience))
        audience = audience[0].upper() + audience[1:]

        temp.append(audience)
        temp.append(scope)
        result.append(temp)

    logger.debug(f"Создание итоговой таблицы {result}")
    return result
