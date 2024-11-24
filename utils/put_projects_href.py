from bs4 import BeautifulSoup


def clean_href(html):
    soup = BeautifulSoup(html, "html.parser")
    projects = soup.find(
        "div", class_="project-list__items project-list__items--column project-list__items--type-projects-page")
    projects_a = projects.findChildren("a", recursive=False)
    projects_href = [project["href"] for project in projects_a]
    projects_href = [
        project for project in projects_href if not project.startswith("https://vk.com/")]
    return projects_href
