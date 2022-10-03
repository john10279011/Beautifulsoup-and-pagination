from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

info = []
r = HTMLSession()
url = "https://www.jumia.co.ke/smartphones/"

info = []


def getpage(url):
    page = r.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def getdata(soup):
    holders = soup.find_all("article", {"class": "prd _fb col c-prd"})
    for item in holders:
        name = item.find("h3", {"class": "name"}).text
        price = item.find("div", {"class": "prc"}).text.replace("KSh", "")
        link = "https://www.jumia.co.ke" + str(
            item.find("a", {"class": "core"})["href"]
        )
        data = {"name": name, "price": price, "links": link}
        info.append(data)
    return


def getnextpage(soup):
    pages = soup.find("div", {"class": "pg-w -ptm -pbxl"})
    url = "https://www.jumia.co.ke" + str(
        pages.find("a", {"aria-label": "Next Page"})["href"]
    )
    return url


try:
    while True:
        soup = getpage(url)
        getdata(soup)
        url = getnextpage(soup)
        if not url:
            break
        else:
            print(url)
except:
    print("all pages done")

all_data = pd.DataFrame(info)
print(all_data)
all_data.to_json("jumiasoup.json")
