from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os

DRIVER_PATH = "C:/Users/Lenovo/Downloads/chromedriver_win32/chromedriver"

options = Options()
options.headless = False
options.add_argument("--window-size=1500,1200")

USER = os.environ['USER']
PASS = os.environ['PASS']

register = input("COURSE: ")
# worklist = input("WORKLIST: ")
dept = register.split(" ")[0].upper()
course = register.split(" ")[1]
section = register.split(" ")[2]

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments")
driver.find_element_by_xpath("//input[@type='IMAGE']").click()
driver.find_element_by_id("username").send_keys(USER)
driver.find_element_by_id("password").send_keys(PASS)
driver.find_element_by_xpath("//input[@type='submit']").click()

timeout = 10

try:
	element_present = EC.presence_of_element_located((By.ID, 'mainTable'))
	WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
	print("TIMEOUT")

def findLink(to_find):
	courses = driver.find_elements_by_tag_name("a")
	for course in courses:
		print(course.text)
		if(course.text == to_find):
			course.click()
			break

findLink(f"{dept}")
findLink(f"{dept} {course}")
findLink(f"{dept} {course} {section}")

# create new worklist if not currently in desired worklist
driver.find_element(By.PARTIAL_LINK_TEXT, 'New Worklist').click()
driver.find_element_by_id("attrWorklistName").send_keys("NEW")
driver.find_element_by_xpath("//input[@value='Create New Worklist']").click()
driver.find_element(By.PARTIAL_LINK_TEXT, f'{dept} {course} {section}').click()

#search for worklist
#!!!


driver.find_element(By.PARTIAL_LINK_TEXT, 'Save To Worklist').click()

# driver.quit()


