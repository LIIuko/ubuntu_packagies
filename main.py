from bs4 import BeautifulSoup
import requests
import graphviz

allPackages = set()

def get_file_dependencies_part1(name_package):

    allPackages.add(name_package)
    UBUNTU_URL = f"https://packages.ubuntu.com/search?keywords={name_package}&searchon=names&suite=jammy&section=all"

    page = requests.get(UBUNTU_URL)
    if page.status_code != 200:
        return None
    text = page.text
    soup = BeautifulSoup(text, "html.parser")
    links_html = soup.find_all('a')

    for link_html in links_html:
        if link_html.get('class') is not None:
            for el in link_html.get('class'):
                if el == "resultlink" and link_html.get('href')[-len(name_package):] == name_package:
                    return link_html.get('href')
    return None


def get_file_dependencies_part2(url_package, name_catalog):
    if url_package is None:
        return

    allPackages.add(name_catalog)
    UBUNTU_PACKAGE_URL = "https://packages.ubuntu.com" + url_package
    name = url_package[:-len(name_catalog)]

    page = requests.get(UBUNTU_PACKAGE_URL)
    if page.status_code != 200:
        return None
    text = page.text
    soup = BeautifulSoup(text, "html.parser")

    local_packages = set()

    links_html = soup.select('ul li dl dt a')
    for link_html in links_html:
        if link_html.text not in allPackages:
            local_packages.add(link_html)
            dot.edge(name_catalog, link_html.text)

    for el in local_packages:
        if el.text not in allPackages:
            print(el.text)
            get_file_dependencies_part2(el.get('href'), el.text)
    return None


if __name__ == '__main__':
    package = input("Введите название пакета для которого нужно вывести дерево зависимостей: ")
    dot = graphviz.Digraph(f'{package} requirements')
    get_file_dependencies_part2(get_file_dependencies_part1(package), package)
    with open(package + ".txt", 'w') as fout:
        fout.write(dot.source)
