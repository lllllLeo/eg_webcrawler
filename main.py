from selenium import webdriver

driver = webdriver.Chrome() # 같은 폴더 아니면 ()안에 경로 넣음
url = 'https://google.com'
driver.get(url)