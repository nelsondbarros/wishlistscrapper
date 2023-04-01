import json

import requests as r
from bs4 import BeautifulSoup


def parse(url):
    """
    Find all items in the wishlist page and return its names and prices.
    :param url:
    The url of the page
    :return tuple:
    Name and price as a tuple
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


def convert_to_json(*args):
    list_object = []
    for i in range(0, len(args[0][0])):
        list_object.append({"item": args[0][0][i], "price": args[0][1][i]})

    with open("wishlist.json", "w") as file:
        file.write(json.dumps(list_object, indent=1))
        return 0


def main():
    url = input("url: ")
    data = parse(url)
    print("Export data to JSON? y/n")
    answer = input("")

    match answer:
        case "n":
            return 0

        case "y":
            convert_to_json(data)
            return 0


if __name__ == "__main__":
    main()
