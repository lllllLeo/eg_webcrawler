from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import telegram
import schedule
import time
import os

# 텔레그램 봇 설정
bot = telegram.Bot(token=os.environ.get("bot_token"))
# 아이디, 비번 설정
eg_login_url = 'https://engoo.co.kr/app/login?automatic=true&redirectTo=%2Fapp%2Foauth%2Fauthorize%3Fclient_id%3Dd2ac7019db25c328dc5d06b1c3c57b7ce1dcb4655d4a2a3c87b7c196875093c7%26display%3D%26intent%3Dlogin%26redirect_uri%3Dhttps%253A%252F%252Fengoo.co.kr%252Fmembers%252Fauth%252Fapp_engoo%252Fcallback%26response_type%3Dcode'

id = '.css-cgadzw'
password = '//*[@id="label-1"]'
signin = '.css-16clkoc'
favorite_teacher = '#main > div.dashboard-container > aside > div.db-sidebar > ul.list-style-none.pd-none.db-sidebar-nav > li:nth-child(4) > a'

my_teacher_list = []
my_teacher_list = "Rena", "Yukino", "Leina", "Mimi", "Keira", "Asaka", "Shinya", "Sayaka", "Yen", "Giselle", "Ilma", "Denny", "Chriss", "Bee Jay", "Franky", "Michelle", "Andrea"

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour='23,0-14', minute='*/29')
def job():
    print("================================== 크롤링 시작")
    GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    now = time.localtime()
    current = "%04d-%02d-%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    print("현재 시간 = ", str(current))

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    # headless, disable-gpu 창숨김모드
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no--sandbox")
    # DevToolsActivePort file doesn't exist 에러 뜨면 밑 두개gi
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    # driver = webdriver.Chrome()
    driver.get(eg_login_url)
    driver.implicitly_wait(2)
    driver.find_element_by_css_selector(id).send_keys(os.environ.get("eg_id"))
    driver.find_element_by_xpath(password).send_keys(os.environ.get("eg_password"))
    driver.find_element_by_css_selector(signin).click()
    driver.find_element_by_css_selector(favorite_teacher).click()

    fav_teachers = []
    fav_teachers = driver.find_elements_by_tag_name('p.teacher-card-teacher-name')  # 즐겨찾는 선생님 수 카운트
    teacher_message = []
    for my_teacher in my_teacher_list:
        print(my_teacher)
        # my_teacher = my_teacher_list[count]
        for count in range(1, len(fav_teachers)):
            teacher = driver.find_element_by_xpath(
                '//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').get_attribute('innerHTML')
            if my_teacher == teacher:
                driver.find_element_by_xpath(
                    '//*[@id="content"]/ul/li[' + str(count) + ']/a').click()  # 선생님 클릭
                getSchedule(driver, teacher_message, my_teacher)
                driver.back()

    # for message in teacher_message:
    driver.quit()
    result_message = "\n".join(teacher_message)
    bot.sendMessage(chat_id=os.environ.get("bot_id"), text=result_message)


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


sched.start()