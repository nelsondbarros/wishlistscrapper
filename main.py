from bs4 import BeautifulSoup
import requests as r
import json
import csv

def parse():

    url = input("url: ")
    url_text = r.get(url).text

    soup = BeautifulSoup(url_text,'lxml')
    items = soup.find_all('li', class_ = 'a-spacing-none g-item-sortable')
    name_list = []
    price_list = []
    for item in items:
        name_list.append(item.find('h2', class_='a-size-base').text.lstrip())
        price_list.append(item.find('span', class_='a-offscreen').text.lstrip())
        #print(f"{name} {price}")
    for n, p  in zip(name_list, price_list):
        print(n, p)
    return name_list, price_list

def convertToJSON(data1, data2):


    list = []
    for i in range(0,len(data1)):
        list.append({"item" : data1[i], "price" : data2[i]})
    with open('wishlist.json', 'w') as file:
        file.write(json.dumps(list, indent=1))
        return 0

#def convertTOCSV(data1, data2):

    
def main():
    data = parse()
    print("Convert data? y/n")
    answer = input("")
    if answer == 'n':
        return 0
    else:
        print("1 - JSON \n2 - CSV")
        answer = input("")
        if answer == '1':
            convertToJSON(data[0], data[1])
            return 0
        # elif answer == '2':
        #     convertTOCSV(data[0], data[1])
        #     return 0


if __name__ == "__main__":
    main()