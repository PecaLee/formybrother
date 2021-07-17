from os import replace
import urllib.request

import requests
from bs4 import BeautifulSoup

hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

URL = "http://anishkapoor.com/"
anishkapoor = requests.get(URL, headers=hdr)

# req = urllib.request.Request(url=URL, headers=hdr)
# anishkapoor = urllib.request.urlopen(req)


def get_works_url():
    soup = BeautifulSoup(anishkapoor.text, "html.parser")
    works = soup.find_all(attrs={"data-target": "works"})

    works_list = []

    for w in works:
        works_list.append(w["href"])

    return works_list


def get_works_data():
    works_list = get_works_url()

    count = 1
    anishkapoorWorks = []

    # 만든 워크리스트를 배열 0번부터 49번까지만 돌린다.
    for url in works_list[0:49]:
        work = requests.get(url)
        soup = BeautifulSoup(work.text, "html.parser")

        title_div = soup.find(attrs={"class": "info works"})
        material_size = soup.find(
            attrs={"class": "block small_text"})

        if material_size:
            material_size = material_size.find("p").text.split("\n")
        else:
            material_size = soup.find(attrs={"class": "block text_block"}).find(
                attrs={"class": "content"}).text.split("\n")

        title = title_div.find("h1").text
        year = title_div.find("p").text
        imgurl = soup.find(attrs={"data-behavior": "gallery"})

        if imgurl:
            imgurl = imgurl.find("img")["data-original"]
            urllib.request.urlretrieve(imgurl, f"./img/{count}.jpg")
            imgNum = f"{count}.jpg"
        else:
            imgNum = "None"

        material = material_size[0].replace("\r", "")

        if len(material_size) > 1:
            size = material_size[1]
        else:
            size = "None"

        workDic = {"title": title, "year": year,
                   "imgNum": imgNum, "material": material, "size": size}

        anishkapoorWorks.append(workDic)

        count = count + 1

    return anishkapoorWorks


print(get_works_data())
