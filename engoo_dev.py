from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import telegram
import schedule
import time
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger
import sys
import os

# import sys, os, time

# exe 파일 만들 때
# if  getattr(sys, 'frozen', False):
#     chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
#     driver = webdriver.Chrome(chromedriver_path)
# else:
#     driver = webdriver.Chrome()

with open('config_.json', 'r') as f:
    config = json.load(f)

# 선생님 이름 설정
# teacher_name = config['TEACHER']['LEINA']
# 텔레그램 봇 설정
bot_token = config['BOT']['TOKEN']
bot_id = config['BOT']['ID']
bot = telegram.Bot(token=bot_token)
# 아이디, 비번 설정
eg_id = config['ENGOO']['ID']
eg_password = config['ENGOO']['PASSWORD']
eg_login_url = config['ENGOO']['LOGIN']
# 아이디, 비번 설정
eg_login_url = 'https://engoo.co.kr/app/login?automatic=true&redirectTo=%2Fapp%2Foauth%2Fauthorize%3Fclient_id%3Dd2ac7019db25c328dc5d06b1c3c57b7ce1dcb4655d4a2a3c87b7c196875093c7%26display%3D%26intent%3Dlogin%26redirect_uri%3Dhttps%253A%252F%252Fengoo.co.kr%252Fmembers%252Fauth%252Fapp_engoo%252Fcallback%26response_type%3Dcode'

id = '.css-cgadzw'
password = '//*[@id="label-1"]'
signin = '.css-16clkoc'
favorite_teacher = '#main > div.dashboard-container > aside > div.db-sidebar > ul.list-style-none.pd-none.db-sidebar-nav > li:nth-child(4) > a'

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
# chrome_options.add_argument('-disable-gpu')
# chrome_options.add_argument('lang=ko_KR')

# driver = webdriver.Chrome(chrome_options=chrome_options)  # 같은 폴더 아니면 ()안에 경로 넣음

my_teacher_list = []
# 일본인 [18]까지
# my_teacher_list = "Rena", "Yukino", "Leina", "Mimi", "Keira", "Taka H", "Yuho", "Kiki", "Asaka", "Yuki", "Shinya", "Shiori G", "Minami S", "Bob", "Sayaka", "Kaiyoh", "Takeru", "Shion", "Yen", "Giselle", "Ilma", "Denny", "Chriss", "Bee Jay", "Franky", "Michelle", "Andrea"
# 프리미엄[7]
my_teacher_list = "Rena", "Yukino", "Leina", "Mimi", "Keira", "Asaka", "Shinya", "Sayaka", "Yen", "Giselle", "Ilma", "Denny", "Chriss", "Bee Jay", "Franky", "Michelle", "Andrea"

sched = BlockingScheduler()


# sched.add_job(job, 'cron', day_of_week='0-6', hour='23,0-14', minute='*/30')
# @sched.scheduled_job('cron', day_of_week='0-6', hour='23,0-14', minute='*/30')
@sched.scheduled_job('cron', day_of_week='mon-sun', hour='17', minute='*/1')
def job():
    print("==================================job() 들어옴")
    # GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
    # CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    now = time.localtime()
    current = "%04d-%02d-%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    print("현재 시간 = ", str(current))
    # print("============================ " + teacher_name + " 선생님 시간표 검색중")
    print("============================ 선생님 시간표 검색중")

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = GOOGLE_CHROME_BIN
    # headless, disable-gpu 창숨김모드
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no--sandbox")
    # DevToolsActivePort file doesn't exist 에러 뜨면 밑 두개gi
    # chrome_options.add_argument("--single-process")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver = webdriver.Chrome()
    driver.get(eg_login_url)
    driver.implicitly_wait(2)
    driver.find_element_by_css_selector(id).send_keys(eg_id)
    driver.find_element_by_xpath(password).send_keys(eg_password)
    driver.find_element_by_css_selector(signin).click()
    driver.find_element_by_css_selector(favorite_teacher).click()
    fav_teachers = []
    fav_teachers = driver.find_elements_by_tag_name('p.teacher-card-teacher-name')  # 즐겨찾는 선생님 수 카운트
    # for count in range(1, len(fav_teachers)):
    #     print(count)
    #     teacher = driver.find_element_by_xpath(
    #         '//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').get_attribute('innerHTML')
    #     for i in my_teacher:
    #         if teacher == i:
    #             driver.find_element_by_xpath(
    #                 '//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').click()  # 선생님 클릭
    #             getSchedule(driver, teacher_message, i)
    #             driver.back()
    #             print(teacher_message)
    teacher_message = []
    print("fav_teacher는  ")
    print(len(fav_teachers))
    for my_teacher in my_teacher_list:
        print(my_teacher)
        # my_teacher = my_teacher_list[count]
        for count in range(1, len(fav_teachers)):
            teacher = driver.find_element_by_xpath(
                '//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').get_attribute('innerHTML')
            print(count)
            if my_teacher == teacher:
                driver.find_element_by_xpath(
                    '//*[@id="content"]/ul/li[' + str(count) + ']/a').click()  # 선생님 클릭
                getSchedule(driver, teacher_message, my_teacher)
                driver.back()
                print(teacher_message)

    # for message in teacher_message:
    driver.quit()
    result_message = "\n".join(teacher_message)
    bot.sendMessage(chat_id=bot_id, text=result_message)


def getSchedule(driver, teacher_message, my_teacher):
    print("============================ getSchedule() 호출")
    reservation_count = []
    reservation_count = driver.find_elements_by_css_selector('a.lessons.label.label-info')
    if len(reservation_count) is 0:
        teacher_message.append(my_teacher + ': X')
        return
    print(my_teacher + '선생님 예약 가능한 시간 수 : %s' % len(reservation_count))

    schedule_list = []
    for j in range(0, len(reservation_count)):
        if len(reservation_count) > 59:
            schedule_list.append('예약 가능 시간 많음 (60개 이상)')
            break
        else:
            schedule = reservation_count[j].find_element_by_xpath('..').find_element_by_xpath(
                '..').find_element_by_css_selector(
                'ul > li:nth-child(1)').get_attribute('innerHTML').replace("<br>", "")
            time = reservation_count[j].find_element_by_xpath('..').get_attribute("id")
            time = time[14:19].replace('-', '시')
            schedule_list.append(schedule + ' ' + time + "분")
    make_message = "\n".join(schedule_list)
    teacher_message.append(my_teacher + '👨‍🏫: %s' % len(reservation_count) + '\n' + make_message)


# @sched.scheduled_job('cron',day_of_week='sun-sat', hour='23,0-14',timezone='America/Chicago')
# def cron_job():
#     sched.add_job(run, "interval", minute='*/30')
# sched.add_job(job, 'cron', day_of_week='mon-sun', hour='17,00', minute='*/1')
# sched.add_job(job, 'cron', day_of_week='0-6', hour='23,0-14', minute='*/1')
# schedule.every(3).minutes.do(job)
# schedule.every(45).seconds.do(job)

sched.start()

# while True:
#     schedule.run_pending()
#     time.sleep(1)
