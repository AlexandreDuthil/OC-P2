import requests
from bs4 import BeautifulSoup
from fonctions import *

book_links = []
book_number = 0
# Récupération des liens de toutes les pages avec des livres, incrémentation d'une liste "links"
categories_links = get_categories_links("https://books.toscrape.com/")

y = 0

for link in categories_links :
    # outil de control du fonctionnement
    y += 1
    print(y)
    # récupération des liens présents sur la première page
    book_links.extend(get_book_links(link))
    book_number += len(get_book_links(link))
    # récupération des liens présents sur les pages suivantes
    if get_page_number(link)>1:
        for i in range(get_page_number(link)-1):
            x = i + 2
            new_link = next_page(link, x)
            book_links.extend(get_book_links(new_link))
            book_number += len(get_book_links(new_link))


print(book_links)
print(book_number)


