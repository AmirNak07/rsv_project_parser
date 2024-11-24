import httpx

from utils import create_table, clean_href, get_href

link = "https://rsv.ru/"
params = {"registration": "true"}

projects_href = get_href(clean_href(httpx.get(link + "competitions/", params=params).content), link)

result = create_table(projects_href)
print(*result, sep="\n\n")
