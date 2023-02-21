import json

import requests as r
from bs4 import BeautifulSoup


def parse():
    url = input("url: ")
    url_text = r.get(url).text

    soup = BeautifulSoup(url_text, "lxml")
    items = soup.find_all("li", class_="a-spacing-none g-item-sortable")
    name_list = []
    price_list = []

    for item in items:
        name_list.append(item.find("h2", class_="a-size-base").text.lstrip())
        price_list.append(item.find("span", class_="a-offscreen").text.lstrip())

    for n, p in zip(name_list, price_list):
        print(n, p)
    return name_list, price_list


def convert_to_json(*args):
    list_object = []
    for i in range(0, len(args)):
        list_object.append({"item": args[0][i], "price": args[1][i]})

    with open("wishlist.json", "w") as file:
        file.write(json.dumps(list_object, indent=1))
        return 0


def main():
    data = parse()
    print("Export data to JSON? y/n")
    answer = input("")

    match answer:
        case "n":
            return 0

        case "y":
            convert_to_json(data[0], data[1])
            return 0


if __name__ == "__main__":
    main()
