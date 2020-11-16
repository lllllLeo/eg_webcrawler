from selenium import webdriver
import json
import telegram
import schedule
import time
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
teacher_name = config['TEACHER']['RENA']
# 텔레그램 봇 설정
bot_token = config['BOT']['TOKEN']
bot_id = config['BOT']['ID']
bot = telegram.Bot(token=bot_token)
# 아이디, 비번 설정
eg_id = config['ENGOO']['ID']
eg_password = config['ENGOO']['PASSWORD']
eg_login_url = config['ENGOO']['LOGIN']

id = '.css-cgadzw'
password = '//*[@id="label-1"]'
signin = '.css-16clkoc'
favorite_teacher = '#main > div.dashboard-container > aside > div.db-sidebar > ul.list-style-none.pd-none.db-sidebar-nav > li:nth-child(4) > a'

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
# chrome_options.add_argument('-disable-gpu')
# chrome_options.add_argument('lang=ko_KR')

# driver = webdriver.Chrome(chrome_options=chrome_options)  # 같은 폴더 아니면 ()안에 경로 넣음



def job():
    now = time.localtime()
    current = "%04d-%02d-%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    print("현재 시간 = ", str(current))
    print("============================ " + teacher_name + " 선생님 시간표 검색중")
    driver = webdriver.Chrome()  # 같은 폴더 아니면 ()안에 경로 넣음
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
    last_result = []
    reservation_count = driver.find_elements_by_css_selector('a.lessons.label.label-info')
    if len(reservation_count) is 0:
        bot.sendMessage(chat_id=bot_id, text=teacher_name + '선생님의 예약 가능한 시간이 없습니다.')
        last_result = reservation_count
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


schedule.every(3).minutes.do(job)
# schedule.every(45).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
