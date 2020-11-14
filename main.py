from selenium import webdriver
import json

with open('config.json','r') as f:
    config = json.load(f)

eg_id = config['ENGOO']['ID']
eg_password = config['ENGOO']['PASSWORD']

driver = webdriver.Chrome() # 같은 폴더 아니면 ()안에 경로 넣음
# Leina https://engoo.co.kr/tutors/39572
# Login https://engoo.co.kr/app/login?automatic=true&redirectTo=%2Fapp%2Foauth%2Fauthorize%3Fclient_id%3Dd2ac7019db25c328dc5d06b1c3c57b7ce1dcb4655d4a2a3c87b7c196875093c7%26display%3D%26intent%3Dlogin%26redirect_uri%3Dhttps%253A%252F%252Fengoo.co.kr%252Fmembers%252Fauth%252Fapp_engoo%252Fcallback%26response_type%3Dcode
url = 'https://engoo.co.kr/app/login?automatic=true&redirectTo=%2Fapp%2Foauth%2Fauthorize%3Fclient_id%3Dd2ac7019db25c328dc5d06b1c3c57b7ce1dcb4655d4a2a3c87b7c196875093c7%26display%3D%26intent%3Dlogin%26redirect_uri%3Dhttps%253A%252F%252Fengoo.co.kr%252Fmembers%252Fauth%252Fapp_engoo%252Fcallback%26response_type%3Dcode'
driver.get(url)
driver.implicitly_wait(3)
driver.find_element_by_css_selector('.css-cgadzw').send_keys(eg_id)
