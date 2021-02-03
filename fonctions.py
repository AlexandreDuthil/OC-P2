import requests
from bs4 import BeautifulSoup
import re


# Récupération des liens de toutes pages catégories avec des livres, incrémentation d'une liste "links"
def get_category_links(url):
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
    del url[-1]
    url.append("page-{}.html".format(str(x)))
    url = ("/").join(url)
    return url

# scraping de la page d'un livre
def book_page_scraper(url,file):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = (soup.find("h1")).text
    category = soup.find("ul").findAll("a")
    category = category[-1].text
    product_description = soup.findAll("p")
    product_description = (product_description[3].text)
    tr_list = soup.findAll("tr")
    td = []
    for tr in tr_list:
        td += tr.find('td')
    universal_product_code = td[0]
    price_including_tax = td[3].replace("Â£","")
    price_excluding_tax = td[2].replace("Â£", "")
    number_available = td[5]
    number_available = re.search("[0-9]+",number_available)
    number_available = number_available.group(0)
    image_url = (soup.find("img"))["src"]
    image_url = image_url.replace("../..", "https://books.toscrape.com")
    review_rating = soup.find("div", {"class": "col-sm-6 product_main"}).findAll("p")
    review_rating = re.search("star-rating [A-Z][a-z]+", str(review_rating))
    review_rating = review_rating.group(0)
    if review_rating == "star-rating Zero": review_rating = 0
    if review_rating == "star-rating One": review_rating = 1
    if review_rating == "star-rating Two": review_rating = 2
    if review_rating == "star-rating Three": review_rating = 3
    if review_rating == "star-rating Four": review_rating = 4
    if review_rating == "star-rating Five": review_rating = 5
    file.write(url+"<"+universal_product_code+"<"+title+"<"+price_including_tax+"<"+price_excluding_tax+"<"+number_available+"<"+product_description+"<"+category+"<"+str(review_rating)+"<"+image_url+"\n")

# récupération du nom de la catégorie via son URL
def get_category_name(url):
    category = re.search("([a-z]+[-])*[a-z]+_[0-9]+", url)
    category = category.group(0)
    category = category.split("_")
    category = category[0]
    return category
