import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import json
import os

url ="https://www.10000recipe.com/recipe/6940325"
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

"""레시피 제목"""
recipe_name = soup.find("title")
recipe_name = recipe_name.get_text()

"""레시피 저장 폴더 생성"""
dir_name = '\\recipe' #임시
#dir_name = '\\'+recipe_name #레시피 제목으로 폴더 생성하기
os.mkdir('C:\\Users\\damin-jo\\Desktop\\Python-WebScraping'+dir_name)
file_path = "C:\\Users\\damin-jo\\Desktop\\Python-WebScraping"

"""레시피 제목 txt파일로 저장"""
with open(file_path+dir_name+"\\recipe_name.txt", "w", encoding="utf-8") as f: 
    f.writelines(recipe_name)

"""레시피 description"""
for tag in soup.find_all("meta"):
    if tag.get("name", None ) =="description":
        recipe_desc = tag.get("content", None)

with open(file_path+dir_name+"\\recipe_description.txt", "w", encoding="utf-8") as f: 
    f.writelines(recipe_desc)

"""레시피 분량/ 시간/ 난이도"""
level = []
recipe_amount = soup.find("span", attrs={"class", "view2_summary_info1"})
recipe_amount = recipe_amount.get_text()
level.append(recipe_amount)
level.append("\n")
recipe_time = soup.find("span", attrs={"class", "view2_summary_info2"})
recipe_time = recipe_time.get_text()
level.append(recipe_time)
level.append("\n")
recipe_lv = soup.find("span", attrs={"class", "view2_summary_info3"})
recipe_lv = recipe_lv.get_text()
level.append(recipe_lv)

with open(file_path+dir_name+"\\recipe_level.txt", "w", encoding="utf-8") as f: 
    f.writelines(level)

"""레시피 재료 저장"""
ingredient = []
amount = []
ingre = soup.find("div", attrs={"class": "ready_ingre3"})
#print(ingre)
with open(file_path+dir_name+"\\recipe_ingre.html", "w", encoding="utf-8") as f:
    f.write(str(ingre))
recipe_file = open(file_path+dir_name+"\\recipe_ingre.html", 'r', encoding='utf-8')
file_soup = BeautifulSoup(recipe_file, 'html.parser')
check = 0
ingre_unit = file_soup.find_all("span", attrs={"class" : "ingre_unit"})
for unit in ingre_unit:
    d = unit.get_text()
    amount.append(d)
    check +=1

ingre_name = file_soup.find_all("li")
for ing in ingre_name:
    if check == 0:
        break
    else:
        a = ing.get_text()
        ingredient.append(a)
        check -=1 
with open(file_path+dir_name+"\\recipe_ingredient.txt", "w", encoding="utf-8") as f:
    f.writelines(ingredient) 

"""img url 저장"""
img_store = []
for i in range(1,20):
    recipe_img = "stepDiv"+str(i)
    recipe = soup.find_all("div",attrs={"id":recipe_img})
    img_store.append(str(recipe))
    img_store.append("\n")

with open(file_path+dir_name+"\\recipe_img.html", "w", encoding="utf-8") as f:
    f.writelines(img_store)
with open(file_path+dir_name+"\\recipe_img.txt", "w", encoding="utf-8") as f:
    f.writelines(img_store)

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

filepath = file_path+dir_name+"\\recipe_img.txt"
target = "https://recipe1.ezmember.co.kr/"
splitdata = fileopen(filepath, target)
step_num = count_word(splitdata, target)

"""img url 추출"""
recipe_file = open(file_path+dir_name+"\\recipe_img.html", 'r', encoding='utf-8')
#저장공간은 위에서 만든 html파일 저장되는 곳으로 수정
file_soup = BeautifulSoup(recipe_file, 'html.parser')

for i in range(0, step_num):
    images = file_soup.findAll('img')[i]
    step_img = images.get("src")
    urllib.request.urlretrieve(step_img, file_path+dir_name+"\\img"+str(i))
    #print(step_img) #테스트용

"""레시피 내용 텍스트 파일로 저장"""
step_store = []
for i in range(1, step_num+1):
    recipe_step = "stepdescr"+str(i)
    recipe = soup.find_all("div",attrs={"id":recipe_step})
    for recipes in recipe:
        a = recipes.get_text()
        #print(a) #test
        step_store.append(a+"\n")
       
with open(file_path+dir_name+"\\recipe.txt", "w", encoding="utf-8") as f:
    f.writelines(step_store)

