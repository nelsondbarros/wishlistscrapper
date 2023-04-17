import json
import sys

import pandas as pd
import requests as r
from bs4 import BeautifulSoup


def scrape_site(url: str) -> tuple:
    """
    Find all items in the wishlist page and return its names and prices.
    :param url: The url of the page
    :return: tuple (Name and price)
    """

    url_text = r.get(url).text

    soup = BeautifulSoup(url_text, "lxml")
    items = soup.find_all("li", class_="a-spacing-none g-item-sortable")
    name_list = []
    price_list = []

    for item in items:
        name_list.append(item.find("h2", class_="a-size-base").text.lstrip())
        if item.find("span", class_="a-offscreen").text is None:
            price_list.append("N/A")
        else:
            price_list.append(item.find("span", class_="a-offscreen").text.lstrip())

    for n, p in zip(name_list, price_list):
        print(n, p)

    if len(name_list) == 0 or len(price_list) == 0:
        raise Exception("Could not retrieve items, please try again!")
    return name_list, price_list


def scrape_to_list(data):
    """
    Return a list of dictionaries from given data
    :param data:
    :return: list
    """

    list_object = []
    for i in range(0, len(data[0][0])):
        list_object.append({"item": data[0][0][i], "price": data[0][1][i]})
    return list_object


def convert_to_json(*args: tuple) -> None:
    """
    Creates a JSON file from given data
    :param args: Tuple returned by scrape function
    :return: None
    """

    list_items = scrape_to_list(args)

    with open("wishlist.json", "w") as file:
        file.write(json.dumps(list_items, indent=1))


def convert_to_csv(*args: tuple) -> None:
    """
    Creates CSV file from given data
    :param args:
    :return: None
    """

    list_items = scrape_to_list(args)

    data_frame = pd.DataFrame(list_items)
    data_frame.to_csv("wishlist.csv")


def main():
    """
    Takes URL as CLI
    :return: int
    """
    url = sys.argv[1]
    data = scrape_site(url)
    print("Export data? 1-JSON, 2-CSV, type e to exit")
    answer = input("")

    match answer:
        case "1":
            convert_to_json(data)

        case "2":
            convert_to_csv(data)

        case "e":
            return 0


if __name__ == "__main__":
    main()
