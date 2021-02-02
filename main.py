import requests
from bs4 import BeautifulSoup
from fonctions import *

# book_links = []
# book_number = 0
# # Récupération des liens de toutes les pages avec des livres, incrémentation d'une liste "links"
# category_links = get_category_links("https://books.toscrape.com/")
#
# y = 0
#
# for link in category_links :
#     # outil de control du fonctionnement
#     y += 1
#     print(y)
#     # récupération des liens présents sur la première page
#     book_links.extend(get_book_links(link))
#     book_number += len(get_book_links(link))
#     # récupération des liens présents sur les pages suivantes
#     if get_page_number(link)>1:
#         for i in range(get_page_number(link)-1):
#             x = i + 2
#             new_link = next_page(link, x)
#             book_links.extend(get_book_links(new_link))
#             book_number += len(get_book_links(new_link))
#
#
# print(book_links)
# print(book_number)

# création du fichier CSV
with open("livres.csv", "w") as file :
    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    file.write("product_page_url, universal_product_code (upc), title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url\n")

# response = requests.get("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# soup = BeautifulSoup(response.text,"html.parser")

book_page_scraper("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", file)

