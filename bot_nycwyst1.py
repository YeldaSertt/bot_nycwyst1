""" This project takes the clues in rows and column of
the puzzle on nytimes.com with BeautifulSoup"""

import logging
import json
import sys
import requests
from bs4 import BeautifulSoup

logging.basicConfig(stream=sys.stdout, format='%(message)s', level=logging.INFO)

URL = requests.get("https://www.nytimes.com/crosswords/GAME/mini")
if URL.status_code == 200:
    SOUP = BeautifulSoup(URL.content, "html.parser")
    GAME = []
    ALLPROP = SOUP.find("section", class_="Layout-clueLists--10_Xl")
    ALLPROP = ALLPROP.find_all("div", class_="ClueList-wrapper--3m-kd")
    for prop in ALLPROP:

        # ACROSS or DOWN
        group = prop.find_all("h3")[0].get_text()
        logging.info(f"> === {group} ===")
        items = prop.find_all("li")
        for item in items:
            js = {}
            number = item.find("span", class_="Clue-label--2IdMY").text
            string = item.find("span", class_="Clue-text--3lZl7").text
            logging.info(f"> {number}. {string}")
            js["group"] = group
            js["number"] = number
            js["string"] = string
            #print(js)
            GAME.append(js)
        with open("bot_nycwyst1.json", "w") as f:
            json.dump(GAME, f)
else:
    logging.error(f" Error : Status Code ==> {URL.status_code}")
