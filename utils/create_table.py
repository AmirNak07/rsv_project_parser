import httpx
from bs4 import BeautifulSoup


def create_table(projects_href):
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
        temp.append(scope)
        temp.append(audience)
        result.append(temp)

    return result
