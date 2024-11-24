import httpx
from bs4 import BeautifulSoup

from utils import get_projects_href

link = "https://rsv.ru/"
params = {"registration": "true"}

projects_href = map(lambda x: x.split("?"), get_projects_href(
    httpx.get(link + "competitions/", params=params).content))
projects_href = [[link + subString[0][1:], dict([subString[1].split("=")])]
                 for subString in projects_href]


for project in projects_href:
    html = httpx.get(project[0], params=project[1]).content
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("h3", class_="project-detail-block__title").text
    text = soup.find("span", class_="detail-image__badge-target_audience").text.strip()
    link = project[0]

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

    print(title)
    print(text)
    print(link)
    print(scope)
    print(audience)
    print("-" * 50)
