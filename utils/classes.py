import requests
from bs4 import BeautifulSoup
import re
import os


class Category:
    book_number = 0

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.books = []
        self.book_links = []
        self.get_book_links(self.url)
        if self.get_page_number(self.url) > 1:
            for i in range(self.get_page_number(self.url)-1):
                x = i + 2
                new_link = self.next_page(self.url, x)
                self.get_book_links(new_link)
        for link in self.book_links:
            self.book_page_scrapper(link)
        self.create_csv()
        Category.book_number += len(self.book_links)
        print(Category.book_number)

    @staticmethod
    def next_page(url, x):
        url = url.split("/")
        del url[-1]
        url.append("page-{}.html".format(str(x)))
        url = "/".join(url)
        return url

    @staticmethod
    def get_page_number(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form")
        book_number = int((form.find("strong")).text)
        page_number = 1 + book_number // 20
        return page_number

    def add_book(self, book):
        self.books.append(book)

    def get_book_links(self, url):
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            ol = soup.find("ol")
            h3s = ol.findAll("h3")
            for h3 in h3s:
                a = h3.find("a")
                link = a["href"]
                # retravail des liens inutilisables sous cette forme
                link = link.split("/")
                del link[0:3]
                link = "/".join(link)
                link = "https://books.toscrape.com/catalogue/" + link
                self.book_links.append(link)
        else:
            print("mauvais URL")

    @staticmethod
    def download_image(url, image_png):
        image = requests.get(url)
        if image.ok:
            if not os.path.exists(image_png):
                with open(image_png, "wb") as img:
                    img.write(image.content)
            else:
                with open(image_png.replace(".png", ".2.png"), "wb") as img:
                    img.write(image.content)

    def book_page_scrapper(self, url):
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            title = (soup.find("h1")).text
            category = soup.find("ul").findAll("a")
            category = category[-1].text
            product_description = soup.findAll("p")
            product_description = product_description[3].text
            tr_list = soup.findAll("tr")
            td = []
            for tr in tr_list:
                td += tr.find('td')
            universal_product_code = td[0]
            price_including_tax = td[3].replace("Â£", "")
            price_excluding_tax = td[2].replace("Â£", "")
            number_available = td[5]
            number_available = re.search("[0-9]+", number_available)
            number_available = number_available.group(0)
            image_url = (soup.find("img"))["src"]
            image_url = image_url.replace("../..", "https://books.toscrape.com")
            self.download_image(image_url, "images/" + title.replace("/", "-") + ".png")
            review_rating = soup.find("div", {"class": "col-sm-6 product_main"}).findAll("p")
            review_rating = re.search("star-rating [A-Z][a-z]+", str(review_rating))
            review_rating = review_rating.group(0)
            if review_rating == "star-rating Zero":
                review_rating = 0
            if review_rating == "star-rating One":
                review_rating = 1
            if review_rating == "star-rating Two":
                review_rating = 2
            if review_rating == "star-rating Three":
                review_rating = 3
            if review_rating == "star-rating Four":
                review_rating = 4
            if review_rating == "star-rating Five":
                review_rating = 5
            self.add_book(
                Book(url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
                     product_description, category, str(review_rating), image_url))

    def create_csv(self):
        with open("donnees_csv/" + self.name + ".csv", "w") as file:
            file.write(
                "product_page_url< universal_product_code (upc)< title< price_including_tax< price_excluding_tax< "
                "number_available< product_description< category< review_rating< image_url\n")
            for book in self.books:
                file.write(
                    book.product_page_url + "<" + book.universal_product_code + "<" + book.title +
                    "<" + book.price_including_tax + "<" + book.price_excluding_tax + "<" +
                    book.number_available + "<" + book.product_description + "<" + book.category +
                    "<" + book.review_rating + "<" + book.image_url + "\n")


class Book:
    def __init__(self, product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                 number_available, product_description, category, review_rating, image_url):
        self.product_page_url = product_page_url
        self.universal_product_code = universal_product_code
        self.title = title
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.number_available = number_available
        self.product_description = product_description
        self.category = category
        self.review_rating = review_rating
        self.image_url = image_url


class Scrapper:
    def __init__(self):
        self.baselink = "https://books.toscrape.com/"
        self.categories = []
        self.get_category_links()

    def get_category_links(self):
        response = requests.get(self.baselink)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            aside = soup.find("aside")
            ahrefs = aside.findAll("a")[1:]
            y = 1
            for a in ahrefs:
                link = "https://books.toscrape.com/" + a["href"]
                self.categories.append(Category(self.get_category_name(link), link))
                print(str(y)+"/50")
                y += 1

    @staticmethod
    def get_category_name(url):
        category = re.search("([a-z]+[-])*[a-z]+_[0-9]+", url)
        category = category.group(0)
        category = category.split("_")
        category = category[0]
        return category
