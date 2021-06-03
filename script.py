from selenium import webdriver
import os
import time
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = "C:/Users/Lenovo/Downloads/chromedriver_win32/chromedriver"

options = Options()
options.headless = False
options.add_argument("--window-size=1500,1200")

USER = os.environ['USER']
PASS = os.environ['PASS']

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://courses.students.ubc.ca/cs/courseschedule")
cwl_login = driver.find_element_by_xpath("//input[@type='IMAGE']").click()
user = driver.find_element_by_id("username").send_keys(USER)
password = driver.find_element_by_id("password").send_keys(PASS)
submit = driver.find_element_by_xpath("//input[@type='submit']").click()
driver.quit()


