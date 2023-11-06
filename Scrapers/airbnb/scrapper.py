from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
import time
from selenium.webdriver.chrome.service import Service
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

id_list = pd.read_csv("reviews.csv")[["reviewer_id", "reviewer_name"]]


service = Service(executable_path=r'chromedriver.exe')
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options, service=service)
driver.get(f'https://www.airbnb.com.sg/login')
driver.find_element(By.XPATH, '//div[contains(text(), "email")]').click()
element = driver.find_element(By.XPATH, '//input[@name="user[email]"]')
for character in "dai90738@zslsz.com":
    element.send_keys(character)
    time.sleep(0.3) # pause for 0.3 seconds
driver.find_element(By.XPATH, '//span[contains(text(), "Continue")]/..').click()
element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="user[password]"]'))
    )
for character in "Password1234":
    element.send_keys(character)
    time.sleep(0.3) # pause for 0.3 seconds

driver.find_element(By.XPATH, '//span[contains(text(), "Log in")]/..').click()
driver.get(f'https://www.airbnb.com.sg/users/show/{id_list.iloc[0, 0]}')
# dai90738@zslsz.com Password1234
write_buf = []
for i in range(id_list.shape[0]):
    if i % 50 == 0:
        with open('user_loc.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(write_buf)
            write_buf = []
    try:
        driver.get(f'https://www.airbnb.com.sg/users/show/{id_list.iloc[i, 0]}')
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{id_list.iloc[i, 1]}")]'))
        )
        if len(driver.find_elements(By.XPATH, '//span[contains(text(), "Lives in")]')) == 0:
            location = ""
        else:
            location = driver.find_element(By.XPATH, '//span[contains(text(), "Lives in")]').text
            location = location.replace("Lives in", "")
        write_buf.append([id_list.iloc[i, 0], location.strip()])
        print(f"Scrapped: {i+1}/{id_list.shape[0]}")
    except Exception as e:
        if len(driver.find_elements(By.XPATH, '//*[contains(text(), "Error code: 404")]')) > 0:
            write_buf.append([id_list.iloc[i, 0], ""])
            print(f"Scrapped: {i+1}/{id_list.shape[0]}")
        else:
            write_buf.append([id_list.iloc[i, 0], ""])
            print(f"Error occured: {i+1}")

with open('user_loc.csv', 'a', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(write_buf)
    write_buf = []





