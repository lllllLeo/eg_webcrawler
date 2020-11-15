from selenium import webdriver
import json
import telegram

with open('config.json', 'r') as f:
    config = json.load(f)
# 선생님 이름 설정
teacher_name = config['TEACHER']['KEIRA']
# 텔레그램 봇 설정
bot_token = config['BOT']['TOKEN']
bot_id = config['BOT']['ID']
bot = telegram.Bot(token=bot_token)
# 아이디, 비번 설정
eg_id = config['ENGOO']['ID']
eg_password = config['ENGOO']['PASSWORD']
eg_login_url = config['ENGOO']['LOGIN']

id = config['HTML']['ID_SELECTOR']
password = '//*[@id="label-1"]'
signin = '.css-16clkoc'
favorite_teacher = '#main > div.dashboard-container > aside > div.db-sidebar > ul.list-style-none.pd-none.db-sidebar-nav > li:nth-child(4) > a'
rena = '#content > ul > li.teacher-favorite-box.teacher-card.teacher-box-39268 > a > div.teacher-card-teacher-info > p.teacher-card-teacher-name'
driver = webdriver.Chrome()  # 같은 폴더 아니면 ()안에 경로 넣음
# Leina https://engoo.co.kr/tutors/39572


url = eg_login_url
driver.get(url)
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
    teacher_uid = driver.find_element_by_css_selector('#favorite-link > a').get_attribute("data-tutor-id")  # 선생님 uid 추출
    reservation_count = []
    reservation_count = driver.find_elements_by_css_selector('a.lessons.label.label-info')
    if len(reservation_count) is 0:
        bot.sendMessage(chat_id=bot_id, text=teacher_name + '선생님의 예약 가능한 시간이 없습니다.')
        return
    print(teacher_name + '선생님 예약 가능한 시간 수 : %s' % len(reservation_count))

    i = 0
    time_list = []
    for i in range(i, len(reservation_count)):
        times = driver.find_elements_by_xpath('//a/parent::li[@id]')  # 예약하기 쪽 뽑아옴
        time = times[i].get_attribute('id').replace("dt_", "").replace("-", "년 ", 1).replace("-", "월 ", 1).replace(
            "_", "일 ", 1).replace("-", "시 ", 1).replace("-00", "분 ", 1)
        time_list.append(time)
    message = "\n".join(time_list)
    bot.sendMessage(chat_id=bot_id, text=message)
    bot.sendMessage(chat_id=bot_id, text="engoo.co.kr\nengoo.co.kr\nengoo.co.kr")
    print(time_list)


def getDate():
    # // *[ @ id = "dt_2020-11-17_10-30-00"] / a 예약하기
    for j in range(2, 9):
        dates = driver.find_elements_by_xpath('//*[@id="teacher_' + teacher_uid + '"]/div[' + str(j) + ']/ul/li[1]')
        # date_list.append(date)
        date = dates[j].find_elements_by_xpath('//a/parent::li[@id]')
        print(date)
    # meme = "\n".join(date)
    # print(meme)
    # time = date.find_elements_by_xpath('//a/parent::li[@id]')
    # print(date.get_attribute('innerHTML').replace("<br>",""))
    # af = time[0].get_attribute('id').replace("dt_", "").replace("-", "년 ", 1).replace("-", "월 ", 1).replace("_", "일 ", 1).replace("-", "시 ", 1).replace("-00", "분 ", 1)
    # print(af)
    # // *[ @ id = "dt_2020-11-17_10-30-00"]
    # // *[ @ id = "dt_2020-11-17_10-30-00"] / a
    # // *[ @ id = "teacher_39572"] / div[4] / ul / li[1]
    # //*[@id="dt_2020-11-17_10-30-00"]


for count in range(1, len(fav_teachers)):
    teacher = driver.find_element_by_xpath('//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').get_attribute(
        'innerHTML')
    if teacher == teacher_name:
        driver.find_element_by_xpath('//*[@id="content"]/ul/li[' + str(count) + ']/a/div[2]/p[1]').click()  # 선생님 클릭
        getSchedule()
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
