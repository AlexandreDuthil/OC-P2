from fonctions import *
import os
if not os.path.exists("images"):
    os.mkdir("images")
if not os.path.exists("donnees_csv"):
    os.mkdir("donnees_csv")

# outil de control du fonctionnement
book_number = 0
# Récupération des liens de toutes les pages avec des livres, incrémentation d'une liste "links"

category_links = get_category_links("https://books.toscrape.com/")

y = 0

for link in category_links :
    # outil de control du fonctionnement
    y += 1
    print(str(y)+"/"+str(len(category_links)))

    # création du fichier CSV au nom de la catégorie

    category = get_category_name(link)
    with open("donnees_csv/"+category+".csv", "w") as file:
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





