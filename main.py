import httpx

from utils import clean_href, create_table, get_href


def main():
    link = "https://rsv.ru/"
    params = {"registration": "true"}

    request = httpx.get(link + "competitions/", params=params)
    if request.status_code == 200:
        request = request.content
    else:
        request.raise_for_status()

    projects = create_table(get_href(clean_href(request), link))

    print(*projects, sep="\n\n")


if __name__ == "__main__":
    main()
