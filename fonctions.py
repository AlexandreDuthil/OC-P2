import requests
from bs4 import BeautifulSoup


# Récupération des liens de toutes pages catégories avec des livres, incrémentation d'une liste "links"
def get_categories_links(url):
    response = requests.get(url)
    if response.ok:
        links = []
        soup = BeautifulSoup(response.text, "html.parser")
        aside = soup.find("aside")
        ahrefs = aside.findAll("a")
        for a in ahrefs:
            link = a["href"]
            links.append("https://books.toscrape.com/" + link)
        del links[0]
    return links

# Récupération du nombre de livres dans la section, et donc du nombre de pages
def get_page_number(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form")
    book_number = int((form.find("strong")).text)
    page_number = 1+book_number//20
    return page_number

# Récupération des liens des pages de tous les livres
def get_book_links(url):
    # récupération des liens de chaque livre
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ol = soup.find("ol")
    h3s = ol.findAll("h3")
    book_links = []
    for h3 in h3s:
        a = h3.find("a")
        link = a["href"]
        # retravaille des liens inutilisables sous cette forme
        link = link.split("/")
        for i in range(3):
            del link[0]
        link = ("/").join(link)
        link = "https://books.toscrape.com/catalogue/" + link
        book_links.append(link)
    return book_links

# modification d'un lien pour passer aux pages suivantes
def next_page(url, x):
    url = url.split("/")
    del url[7]
    url.append("page-{}.html".format(str(x)))
    url = ("/").join(url)
    return url



