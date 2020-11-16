from selenium import webdriver
import json
import telegram
import sys, os, time

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
rena = '#content > ul > li.teacher-favorite-box.teacher-card.teacher-box-39268 > a > div.teacher-card-teacher-info > p.teacher-card-teacher-name'

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
# chrome_options.add_argument('-disable-gpu')
# chrome_options.add_argument('lang=ko_KR')

# driver = webdriver.Chrome(chrome_options=chrome_options)  # 같은 폴더 아니면 ()안에 경로 넣음
driver = webdriver.Chrome()  # 같은 폴더 아니면 ()안에 경로 넣음
driver.get(eg_login_url)
driver.implicitly_wait(3)
driver.find_element_by_css_selector(id).send_keys(eg_id)
driver.find_element_by_xpath(password).send_keys(eg_password)
driver.find_element_by_css_selector(signin).click()
driver.find_element_by_css_selector(favorite_teacher).click()
fav_teachers = []
fav_teachers = driver.find_elements_by_tag_name('p.teacher-card-teacher-name')  # 즐겨찾는 선생님 수 카운트
teacher_uid = ''


def getSchedule():
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
        schedule = reservation_count[i].find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_css_selector(
            'ul > li:nth-child(1)').get_attribute('innerHTML').replace("<br>", "")
        time = reservation_count[i].find_element_by_xpath('..').get_attribute("id")
        time = time[14:19].replace('-','시')
        schedule_list.append(schedule + " " + time + "분")
    message = "\n".join(schedule_list)
    bot.sendMessage(chat_id=bot_id, text=teacher_name + '👨‍🏫  가능한 타임 : %s' % len(reservation_count) + '\n' + message)
    bot.sendMessage(chat_id=bot_id, text="engoo.co.kr\nengoo.co.kr\nengoo.co.kr")
    print(schedule_list)


print("============================ " + teacher_name + " 선생님 시간표 검색중")
for count in range(1, len(fav_teachers)):
    teacher = driver.find_element_by_xpath('//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').get_attribute(
        'innerHTML')
    if teacher == teacher_name:
        driver.find_element_by_xpath('//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').click()  # 선생님 클릭
        getSchedule()
        # getDate()
        driver.quit()
        break

# print(a[i].get_attribute('id'))

# print(a[i].find_element_by_xpath('//a/parent::li[@id]').get_attribute('id'))

# print(i.get_attribute('innerHTML'))
# // *[ @ id = "dt_2020-11-17_10-30-00"]
# // *[ @ id = "dt_2020-11-17_10-00-00"] xpath
# #dt_2020-11-17_10-00-00 selector
# //*[@id="dt_2020-11-17_10-00-00"]/div 예약됨 xpath
# #dt_2020-11-17_10-00-00 > div 예약됨 셀렉터
#  # dt_2020-11-17_10-30-00 > a 예약하기 셀렉터
#  // *[ @ id = "dt_2020-11-17_10-30-00"] / a  예약하기 xpath

#     .find_elements_by_css_selector('a.lessons label label-info').get_attribute("innerHTML")
# driver.find_element_by_css_selector()
# for j in range(1, )
# driver.

# dt_2020-11-17_10-30-00 > a
# //*[@id="teacher_39572"]/div[1]  #teacher_39572 > div:nth-child(1)
# //*[@id="teacher_39572"]/div[2]


# 즐겨찾기 선생님에서 uid뺴오기
# teacher_uid = driver.find_element_by_css_selector('#content > ul > li').get_attribute("class")
#         teacher_uid = teacher_uid[-5:]

# time_count = driver.find_element_by_xpath('// *[ @ id = "teacher_'+str(teacher_uid)+'"] / div[1] / ul / li[22]').get_attribute('innerHTML')
# print(time_count) # 10:00

#   // *[ @ id = "teacher_39572"] / div[1] / ul / li[22]  10:00부터
#   // *[ @ id = "teacher_39572"] / div[1] / ul / li[49]  23:30까지
