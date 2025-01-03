from loguru import logger


def get_href(dry_html: list, link: str) -> list:
    projects_href = map(lambda x: x.split("?"), dry_html)
    projects_href = [[link + i[0][1:], dict([i[1].split("=")])] for i in projects_href]
    logger.debug("Обработка ссылок с проектами")
    return projects_href
