from selenium import webdriver
import json
import telegram
import schedule
import time
import os
# import sys, os, time

# exe 파일 만들 때
# if  getattr(sys, 'frozen', False):
#     chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
#     driver = webdriver.Chrome(chromedriver_path)
# else:
#     driver = webdriver.Chrome()

# with open('config_.json', 'r') as f:
#     config = json.load(f)

# 선생님 이름 설정
teacher_name = ''
# 텔레그램 봇 설정
bot_token = ''
bot_id = ''
bot = ''
# 아이디, 비번 설정
eg_id = ''
eg_password = ''
eg_login_url = 'https://engoo.co.kr/app/login?automatic=true&redirectTo=%2Fapp%2Foauth%2Fauthorize%3Fclient_id%3Dd2ac7019db25c328dc5d06b1c3c57b7ce1dcb4655d4a2a3c87b7c196875093c7%26display%3D%26intent%3Dlogin%26redirect_uri%3Dhttps%253A%252F%252Fengoo.co.kr%252Fmembers%252Fauth%252Fapp_engoo%252Fcallback%26response_type%3Dcode'

id = '.css-cgadzw'
password = '//*[@id="label-1"]'
signin = '.css-16clkoc'
favorite_teacher = '#main>div.dashboard-container>aside>div.db-sidebar>ul.list-style-none.pd-none.db-sidebar-nav>li:nth-child(4)>a'

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
# chrome_options.add_argument('-disable-gpu')
# chrome_options.add_argument('lang=ko_KR')

# driver = webdriver.Chrome(chrome_options=chrome_options)  # 같은 폴더 아니면 ()안에 경로 넣음



def job():
    GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    now = time.localtime()
    current = "%04d-%02d-%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    print("현재 시간 = ", str(current))
    print("============================ " + teacher_name + " 선생님 시간표 검색중")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no--sandbox")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver.get(eg_login_url)
    driver.implicitly_wait(2)
    driver.find_element_by_css_selector(id).send_keys(eg_id)
    driver.find_element_by_xpath(password).send_keys(eg_password)
    driver.find_element_by_css_selector(signin).click()
    driver.find_element_by_css_selector(favorite_teacher).click()
    fav_teachers = []
    fav_teachers = driver.find_elements_by_tag_name('p.teacher-card-teacher-name')  # 즐겨찾는 선생님 수 카운트
    for count in range(1, len(fav_teachers)):
        teacher = driver.find_element_by_xpath(
            '//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').get_attribute(
            'innerHTML')
        if teacher == teacher_name:
            driver.find_element_by_xpath('//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').click()  # 선생님 클릭
            getSchedule(driver)
            driver.quit()
            break


def getSchedule(driver):
    print("============================ getSchedule() 호출")

    reservation_count = []
    reservation_count = driver.find_elements_by_css_selector('a.lessons.label.label-info')
    if len(reservation_count) is 0:
        bot.sendMessage(chat_id=bot_id, text=teacher_name + '선생님의 예약 가능한 시간이 없습니다.')

        return
    print(teacher_name + '선생님 예약 가능한 시간 수 : %s' % len(reservation_count))

    i = 0
    schedule_list = []
    for i in range(i, len(reservation_count)):
        schedule = reservation_count[i].find_element_by_xpath('..').find_element_by_xpath(
            '..').find_element_by_css_selector(
            'ul > li:nth-child(1)').get_attribute('innerHTML').replace("<br>", "")
        time = reservation_count[i].find_element_by_xpath('..').get_attribute("id")
        time = time[14:19].replace('-', '시')
        schedule_list.append(schedule + " " + time + "분")
    message = "\n".join(schedule_list)
    bot.sendMessage(chat_id=bot_id, text=teacher_name + '👨‍🏫  가능한 타임 : %s' % len(reservation_count) + '\n' + message)
    bot.sendMessage(chat_id=bot_id, text="engoo.co.kr\nengoo.co.kr\nengoo.co.kr")
    print(schedule_list)


# schedule.every(3).minutes.do(job)
schedule.every(45).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
