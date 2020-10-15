import requests
from bs4 import BeautifulSoup
#import re
import urllib.request
from urllib.request import Request, urlopen
import json
import os
url ="https://www.10000recipe.com/recipe/6940325"
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

"""레시피 저장 폴더 생성"""
dir_name = '\\recipe' #임시
os.mkdir('C:\\Users\\damin-jo\\Desktop\\Python-WebScraping'+dir_name)

"""img url 저장"""
img_store = []
for i in range(1,20):
    recipe_img = "stepDiv"+str(i)
    recipe = soup.find_all("div",attrs={"id":recipe_img})
    img_store.append(str(recipe))
    img_store.append("\n")

with open("C:\\Users\\damin-jo\\Desktop\\Python-WebScraping"+dir_name+"\\recipe_img.html", "w", encoding="utf-8") as f:
    f.writelines(img_store)# 
with open("C:\\Users\\damin-jo\\Desktop\\Python-WebScraping"+dir_name+"\\recipe_img.txt", "w", encoding="utf-8") as f:
    f.writelines(img_store)#

def fileopen(data, target):
    with open(data, 'r', encoding='UTF-8') as file:
        text = file.read()
        if target in text:
            splitdata = text.split()
    return splitdata

def count_word(data, target):
    count =0
    for i in data:
        if target in i:
            count += 1
    return count

filepath = "C:\\Users\\damin-jo\\Desktop\\Python-WebScraping"+dir_name+"\\recipe_img.txt"
target = "https://recipe1.ezmember.co.kr/"
splitdata = fileopen(filepath, target)
step_num = count_word(splitdata, target)

"""img url 추출"""
recipe_file = open("C:\\Users\\damin-jo\\Desktop\\Python-WebScraping"+dir_name+"\\recipe_img.html", 'r', encoding='utf-8')
#저장공간은 위에서 만든 html파일 저장되는 곳으로 수정
soup = BeautifulSoup(recipe_file, 'html.parser')

for i in range(0, step_num):
    images = soup.findAll('img')[i]
    step_img = images.get("src")
    urllib.request.urlretrieve(step_img, "C:\\Users\\damin-jo\\Desktop\\Python-WebScraping"+dir_name+"\\img"+str(i))
    #print(step_img) #테스트용

"""레시피 내용 텍스트 파일로 저장"""
step_store = []
for i in range(1, step_num+1):
    recipe_step = "stepdescr"+str(i)
    recipe = soup.find_all("div",attrs={"id":recipe_step})
    for recipes in recipe:
        a = recipes.get_text()
        #print(a)
        step_store.append(a+"\n") #list안에 원소 없는 상태에서 store[i]=a로 지정 불가
       
with open("C:\\Users\\damin-jo\\Desktop\\Python-WebScraping"+dir_name+"\\recipe.txt", "w", encoding="utf-8") as f:
    f.writelines(step_store)# 

