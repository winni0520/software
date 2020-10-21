from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
import urllib.request
from urllib.request import Request, urlopen
import json
import os

driver = webdriver.Chrome('C:\\Users\\damin-jo\\Desktop\\Selenium\\chromedriver_win32\\chromedriver.exe')
file_path = input("데이터 저장할 경로 입력(절대경로): ")
total_recipe_num = input("웹 크롤링하고 싶은 레시피 개수 입력: ")
total_recipe_num = int(total_recipe_num)
while total_recipe_num >0:
    category_url = ""
    print("웹 크롤링할 레시피 분류 입력(숫자)")
    print("[1.국/탕 2.밑반찬 3.디저트 4.양식 5.메인 반찬 6.찌개]")
    print("[7.면/만두 8.밥/죽/떡 9.퓨전 10.김치/젓갈/장류 11.양념/소스/잼]")
    print("[12.샐러드 13.스프 14.빵 15.과자 16.차/음료/술 17.기타]")
    category = input(":")
    category = int(category)
    recipe_num = input("해당 분류 웹 크롤링하고 싶은 레시피 개수 입력(전체 페이지 개수: {0}): ".format(total_recipe_num))
    recipe_num = int(recipe_num)
    """
    category_check = []
    category_check.append(category)
    number_check = []
    number_check.append(recipe_num) #중복 폴더 생성 방지용
    """
    while category_url == "":
        if category == 1: #국/탕
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=54&order=reco&page="
            folder_name = "tang"
        elif category == 2: #밑반찬
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=63&order=reco&page="
            folder_name = "sidedish"
        elif category == 3: #디저트
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=60&order=reco&page="
            folder_name = "dessert"
        elif category == 4: #양식
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=65&order=reco&page="
            folder_name = "western"
        elif category == 5: #메인 반찬
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=56&order=reco&page="
            folder_name = "main_sidedish"
        elif category == 6: #찌개
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=55&order=reco&page="
            folder_name = "jjigae"
        elif category == 7: #면/만두
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=53&order=reco&page="
            folder_name = "noodle"
        elif category == 8: #밥/죽/떡
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=52&order=reco&page="
            folder_name = "rice"
        elif category == 9: #퓨전
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=61&order=reco&page="
            folder_name = "fushion"
        elif category == 10: #김치/젓갈/장류
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=57&order=reco&page="
            folder_name = "kimchi"
        elif category == 11: #양념/소스/잼
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=58&order=reco&page="
            folder_name = "sauce"
        elif category == 12: #샐러드
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=64&order=reco&page="
            folder_name = "salad"
        elif category == 13: #스프
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=68&order=reco&page="
            folder_name = "soup"
        elif category == 14: #빵
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=66&order=reco&page="
            folder_name = "bread"
        elif category == 15: #과자
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=69&order=reco&page="
            folder_name = "snack"
        elif category == 16: #차/음료/술
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=59&order=reco&page="
            folder_name = "drink"
        elif category == 17: #기타
            category_url = "https://www.10000recipe.com/recipe/list.html?cat4=62&order=reco&page="
            folder_name = "etc"
        else:
            category == input("입력을 잘못했습니다. 다시 입력해주세요. :")
    page = 1
    number = 0 #folder
    while category >0:
        
        driver.get(category_url+str(page))
        time.sleep(1) #url loading wait
        html = driver.page_source
        cate_soup = BeautifulSoup(html, 'lxml')

        """카테고리 페이지에서 레시피 url 긁어오기"""
        titles = cate_soup.find_all("a", attrs={"class":"common_sp_link"}) #일반 레시피
        recipe_url = []
        for title in titles:
            url = title.get("href")
            recipe_url.append(url)

        complete_url = "https://www.10000recipe.com"
        for i in range(len(recipe_url)):
            recipe_url[i] = complete_url+recipe_url[i]
    
        go_category = recipe_num // 40 
        category_rest = category - go_category*40
        store_page = [] #어느 페이지까지 크롤링 해야하는지 저장
        for i in range(go_category+1):
            store_page.append(i+1)
        
        if go_category >=1:
            for i in range(40):
                """레시피 저장"""
                url = recipe_url[i]
                res = requests.get(url)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, "lxml")

                """레시피 제목"""
                recipe_name = soup.find("title")
                recipe_name = recipe_name.get_text()

                """레시피 저장 폴더 생성"""
                folder_number = str(number).zfill(3)
                dir_name = '\\'+folder_name+folder_number
                number +=1
                os.mkdir(file_path+dir_name)

                """레시피 url 저장"""
                with open(file_path+dir_name+"\\recipe_url.txt", "w", encoding="utf-8") as f: 
                    f.writelines(url)

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
                if recipe_amount != None:
                    recipe_amount = recipe_amount.get_text()
                    level.append(recipe_amount)
                    level.append("\n")
                
                recipe_time = soup.find("span", attrs={"class", "view2_summary_info2"})
                if recipe_time != None:
                    recipe_time = recipe_time.get_text()
                    level.append(recipe_time)
                    level.append("\n")
                recipe_lv = soup.find("span", attrs={"class", "view2_summary_info3"})
                if recipe_lv != None:
                    recipe_lv = recipe_lv.get_text()
                    level.append(recipe_lv)

                with open(file_path+dir_name+"\\recipe_level.txt", "w", encoding="utf-8") as f: 
                    f.writelines(level)

                """레시피 재료 저장"""
                ingredient = []
                amount = []
                ingre = soup.find("div", attrs={"class": "ready_ingre3"})
                with open(file_path+dir_name+"\\recipe_ingre.html", "w", encoding="utf-8") as f:
                    f.write(str(ingre))
                recipe_file = open(file_path+dir_name+"\\recipe_ingre.html", 'r', encoding='utf-8')
                i_file_soup = BeautifulSoup(recipe_file, 'html.parser')
                check = 0
                ingre_unit = i_file_soup.find_all("span", attrs={"class" : "ingre_unit"})
                for unit in ingre_unit:
                    d = unit.get_text()
                    amount.append(d)
                    check +=1

                ingre_name = i_file_soup.find_all("li")
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
                file_soup = BeautifulSoup(recipe_file, 'html.parser')

                for i in range(0, step_num):
                    images = file_soup.findAll('img')[i]
                    step_img = images.get("src")
                    urllib.request.urlretrieve(step_img, file_path+dir_name+"\\img"+str(i)+".png")

                """레시피 내용 텍스트 파일로 저장"""
                step_store = []
                for i in range(1, step_num+1):
                    recipe_step = "stepdescr"+str(i)
                    recipe = soup.find_all("div",attrs={"id":recipe_step})
                    for recipes in recipe:
                        a = recipes.get_text()
                        step_store.append(a+"\n")
                    
                with open(file_path+dir_name+"\\recipe.txt", "w", encoding="utf-8") as f:
                    f.writelines(step_store)

            recipe_num = recipe_num - 40
            page = store_page[page]
            go_category -=1
            total_recipe_num -= 40
            
        else:
            for i in range(recipe_num):
                """레시피 저장"""
                url = recipe_url[i]
                res = requests.get(url)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, "lxml")

                """레시피 제목"""
                recipe_name = soup.find("title")
                recipe_name = recipe_name.get_text()

                """레시피 저장 폴더 생성"""
                
                folder_number = str(number).zfill(3)
                dir_name = '\\'+folder_name+folder_number
                number +=1
                os.mkdir(file_path+dir_name)

                """레시피 url 저장"""
                with open(file_path+dir_name+"\\recipe_url.txt", "w", encoding="utf-8") as f: 
                    f.writelines(url)

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
                if recipe_amount != None:
                    recipe_amount = recipe_amount.get_text()
                    level.append(recipe_amount)
                    level.append("\n")
                
                recipe_time = soup.find("span", attrs={"class", "view2_summary_info2"})
                if recipe_time != None:
                    recipe_time = recipe_time.get_text()
                    level.append(recipe_time)
                    level.append("\n")
                recipe_lv = soup.find("span", attrs={"class", "view2_summary_info3"})
                if recipe_lv != None:
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
                i_file_soup = BeautifulSoup(recipe_file, 'html.parser')
                check = 0
                ingre_unit = i_file_soup.find_all("span", attrs={"class" : "ingre_unit"})
                for unit in ingre_unit:
                    d = unit.get_text()
                    amount.append(d)
                    check +=1

                ingre_name = i_file_soup.find_all("li")
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
                file_soup = BeautifulSoup(recipe_file, 'html.parser')

                for i in range(0, step_num):
                    images = file_soup.findAll('img')[i]
                    step_img = images.get("src")
                    urllib.request.urlretrieve(step_img, file_path+dir_name+"\\img"+str(i)+".png")

                """레시피 내용 텍스트 파일로 저장"""
                step_store = []
                for i in range(1, step_num+1):
                    recipe_step = "stepdescr"+str(i)
                    recipe = soup.find_all("div",attrs={"id":recipe_step})
                    for recipes in recipe:
                        a = recipes.get_text()
                        step_store.append(a+"\n")
                    
                with open(file_path+dir_name+"\\recipe.txt", "w", encoding="utf-8") as f:
                    f.writelines(step_store)
            total_recipe_num -= recipe_num  
            category = 0
            page = 1 #초기화