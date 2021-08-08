from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

group= 'Python Code'
session_file_path="user-data-dir=C:\\Users\\syedi\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\WhatBot"

options=webdriver.FirefoxOptions()
options.add_argument(session_file_path)

browser = webdriver.Firefox(
    executable_path= "C:\\Users\\syedi\\Documents\\Python\\geckodriver.exe",options=options)
browser.maximize_window()
browser.get('https://web.whatsapp.com/')
time.sleep(1)
search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

search_box = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )
group_xpath = f'//span[@title="{group}"]'
search_box.send_keys(group)
time.sleep(1)
group_title = browser.find_element_by_xpath(group_xpath)
group_title.click()

input_xpath='//div[@contenteditable="true"][@data-tab="6"]'
input_box=browser.find_element_by_xpath(input_xpath)
input_box.send_keys("Test by Imran")
time.sleep(1)
input_box.send_keys(Keys.ENTER)

#search_box.send_keys(Keys.CONTROL+"v")
