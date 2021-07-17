from os import replace
import urllib.request

import requests
from bs4 import BeautifulSoup

hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
URL = "http://anishkapoor.com/"
anishkapoor = requests.get(URL, headers=hdr)
# 리퀘스트로 anishkapoor.com의 데이터를 받아옴


def get_works_url():
    soup = BeautifulSoup(anishkapoor.text, "html.parser")
    works = soup.find_all(attrs={"data-target": "works"})
    # BeautifulSoup로 파싱한 데이터를 soup에 할당
    # data-targe="works"를 가지고 있는 것들을 모두 찾아 works에 할당

    works_list = []
    # 리스트를 만들어 준비

    for w in works:
        works_list.append(w["href"])
    # for문으로 works리스트를 하나하나 돌면서 url을 가져와 works_list에 밀어넣는다.

    return works_list
    # works_list를 리턴


def get_works_data():
    works_list = get_works_url()
    # works_list에 get_works_url함수의 리턴값을 할당

    count = 1
    anishkapoorWorks = []
    # count값과 데이터리스트를 만들어 준비

    for url in works_list[0:49]:
        # 만든 워크리스트를 배열 0번부터 49번까지만 돌린다.
        work = requests.get(url)
        soup = BeautifulSoup(work.text, "html.parser")
        # 각 작품의 링크를 가져와 해석
        # 밑은 각각의 필요한 정보를 찾기
        # if로 조건을 주어 에러 피하기

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
        # 각각의 필요한 정보를 딕셔너리 타입에 정리

        anishkapoorWorks.append(workDic)
        # 만든 딕셔너리 타입의 데이터를 리스트에 저장

        count = count + 1
        # 카운팅 숫자 올리기

    return anishkapoorWorks
    # 정보 리턴


print(get_works_data())
