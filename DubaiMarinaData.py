from bs4 import BeautifulSoup
import requests, re, json

BASE_URL = "https://www.propertyfinder.ae"

page = requests.get("https://www.propertyfinder.ae/en/search?c=1&l=50&ob=mr&page=2&t=1")
content = page.content
soup = BeautifulSoup(content, 'html.parser')

pagination = soup.find("div",{"class":"pagination_links"}).findAll("a",{"class":"pagination_link"})

index = 0
lastIndex = 0;

while True:

    pageIndex = 0;
    
    if int(pagination[len(pagination) - 1].text) == lastIndex:
        break;

    for page in pagination:
        pageURL = BASE_URL + page['href']

        pageIndex += 1;
        if int(page.text) > lastIndex:

            print ("Page: {} - LastIndex : {}".format(page.text, lastIndex))
            propertyPage = requests.get(pageURL)
            pageSoup = BeautifulSoup(propertyPage.content, 'html.parser')


            for item in pageSoup.findAll("div",{"class":"cardlist_item"}):
                index += 1;
                url = BASE_URL.encode("utf-8") + item.find("a")['href'].encode("utf-8")
                price = item.find("span",{"class":"card_pricevalue"}).get_text()
                print("Count: {}\nURL: {}\nPrice: {}\n".format(index,url, price))


            print("PageIndex: {}".format(pageIndex))
            if pageIndex == len(pagination):
                lastIndex = int(page.text)
                pagination = pageSoup.find("div",{"class":"pagination_links"}).findAll("a",{"class":"pagination_link"})