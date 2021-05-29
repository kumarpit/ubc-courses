from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os 
import wget

driver = webdriver.Chrome("C:/Users/Lenovo/Downloads/chromedriver_win32/chromedriver.exe")
driver.get("https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSRVSSCFramework")

# select input fields and wait for web page to fully load
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

# clear input fields
username.clear()
password.clear()

# send username, password, click login
username.send_keys(os.environ.get("USER"))
password.send_keys(os.environ.get("PASS"))

# click login
login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

