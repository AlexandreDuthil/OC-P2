from utils.classes import Scrapper
import os

if not os.path.exists("images"):
    os.mkdir("images")
if not os.path.exists("donnees_csv"):
    os.mkdir("donnees_csv")

my_scrapper = Scrapper()
