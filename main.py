from selenium import webdriver
import win32com.client
from selenium.webdriver.common.keys import Keys
import json
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By

with open('config.json','r') as f:
    config = json.load(f)

eg_id = config['ENGOO']['ID']
eg_password = config['ENGOO']['PASSWORD']

login = 'https://engoo.co.kr/app/login?automatic=true&redirectTo=%2Fapp%2Foauth%2Fauthorize%3Fclient_id%3Dd2ac7019db25c328dc5d06b1c3c57b7ce1dcb4655d4a2a3c87b7c196875093c7%26display%3D%26intent%3Dlogin%26redirect_uri%3Dhttps%253A%252F%252Fengoo.co.kr%252Fmembers%252Fauth%252Fapp_engoo%252Fcallback%26response_type%3Dcode'
id = '.css-cgadzw'
password = '//*[@id="label-1"]'
signin = '.css-16clkoc'
favorite_teacher = '#main > div.dashboard-container > aside > div.db-sidebar > ul.list-style-none.pd-none.db-sidebar-nav > li:nth-child(4) > a'
rena = '#content > ul > li.teacher-favorite-box.teacher-card.teacher-box-39268 > a > div.teacher-card-teacher-info > p.teacher-card-teacher-name'
driver = webdriver.Chrome() # 같은 폴더 아니면 ()안에 경로 넣음
# Leina https://engoo.co.kr/tutors/39572
url = login
driver.get(url)
driver.implicitly_wait(3)
driver.find_element_by_css_selector(id).send_keys(eg_id)
driver.find_element_by_xpath(password).send_keys(eg_password)
driver.find_element_by_css_selector(signin).click()
driver.find_element_by_css_selector(favorite_teacher).click()
#content > ul > li.teacher-favorite-box.teacher-card.teacher-box-39268 > a > div.teacher-card-teacher-info > p.teacher-card-teacher-name
# ii = driver.find_elements_by_css_selector('#content > ul > li.teacher-favorite-box.teacher-card.teacher-box-39268 > a > div.teacher-card-teacher-info > p.teacher-card-teacher-name').get_attribute("innerHTML")
fav_teachers = []
fav_teachers = driver.find_elements_by_tag_name('p.teacher-card-teacher-name') # 즐겨찾는 선생님 수 카운트

# teacher_uid = driver.find_element_by_css_selector('#content > ul > li').get_attribute("class")
# teacher_uid[-5:]
# dd = ii[-1:-5]

# //*[@id="content"]/ul/li[4]
# //*[@id="content"]/ul/li[4]/a/div[2]/p[1]
# //*[@id="content"]/ul/li[14]/a/div[2]/p[1]

#teacher_39572 > div:nth-child(1) > ul > li.t-10\:00
#teacher_39572 > div:nth-child(1) > ul > li.t-10\:30
#teacher_39572 > div:nth-child(1) > ul > li.t-10\:30
#teacher_39572 > div:nth-child(1) > ul > li.t-11\:00
for count in range(1, len(fav_teachers)):
    teacher = driver.find_element_by_xpath('//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').get_attribute('innerHTML')
    if (teacher == 'Leina'):
        # time_count = []
        driver.find_element_by_xpath('//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').click() # 선생님 클릭
        teacher_uid = driver.find_element_by_css_selector('#favorite-link > a').get_attribute("data-tutor-id") # 선생님 uid 추출
        time_count = driver.find_element_by_css_selector('#teacher_'+str(teacher_uid)+' > div:nth-child(1) > ul > li').get_attribute('innerHTML')
        print(time_count)
        # for day in range(1, 7):
        #     hh = driver.find_element_by_xpath('//*[@id="teacher_' + str(teacher_uid) +'"]/div[' + str(day) + ']')
        #     for time in
        #     hh.find_element_by_css_selector('a.lessons label label-info').get_attribute("innerHTML")
        #     print(hh)


        #     .find_elements_by_css_selector('a.lessons label label-info').get_attribute("innerHTML")
        # driver.find_element_by_css_selector()
        # for j in range(1, )
        # driver.

#dt_2020-11-17_10-30-00 > a
# //*[@id="teacher_39572"]/div[1]  #teacher_39572 > div:nth-child(1)
# //*[@id="teacher_39572"]/div[2]



# 즐겨찾기 선생님에서 uid뺴오기
# teacher_uid = driver.find_element_by_css_selector('#content > ul > li').get_attribute("class")
#         teacher_uid = teacher_uid[-5:]