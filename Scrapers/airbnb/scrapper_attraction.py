from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
import time
from selenium.webdriver.chrome.service import Service
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path=r'chromedriver.exe')
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options, service=service)
arr =[]
for i in range(10):
    driver.get(f'https://www.tripadvisor.com/Search?q=Dallas%2C%20Texas%2C%20USA&ssrc=A&geo=1&o={i*30}')
    time.sleep(5)
    elts = driver.find_elements(By.XPATH, '//div[@class="location-meta-block"]')
    for t in elts:
        title = t.find_element(By.XPATH,'./div[@class="result-title"]/span').text
        arr.append(title)

pd.DataFrame(arr).to_csv('attractions.csv')


