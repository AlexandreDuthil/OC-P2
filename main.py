import requests
from bs4 import BeautifulSoup
from fonctions import *

book_number = 0
# Récupération des liens de toutes les pages avec des livres, incrémentation d'une liste "links"
category_links = get_category_links("https://books.toscrape.com/")

y = 0

for link in category_links :
    # outil de control du fonctionnement
    y += 1
    print(y)


    # création du fichier CSV au nom de la catégorie
    category = get_category_name(link)
    with open("donnees/"+category+".csv", "w") as file:
        file.write(
            "product_page_url< universal_product_code (upc)< title< price_including_tax< price_excluding_tax< number_available< product_description< category< review_rating< image_url\n")


        # récupération des liens présents sur la première page
        book_links = get_book_links(link)
        for link2 in book_links:
            book_page_scraper(link2, file)
        book_number += len(get_book_links(link))


        # récupération des liens présents sur les pages suivantes
        if get_page_number(link)>1:
            for i in range(get_page_number(link)-1):
                x = i + 2
                new_link = next_page(link, x)
                book_links = get_book_links(new_link)

                for link3 in book_links:
                    book_page_scraper(link3, file)
                book_number += len(get_book_links(new_link))

print(book_number)

# response = requests.get("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# soup = BeautifulSoup(response.text, "html.parser")
# product_description = soup.findAll("p")
# product_description = (product_description)[3]
# print(product_description)





