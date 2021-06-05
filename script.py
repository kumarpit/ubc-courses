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

def findLink(to_find, driver):
	courses = driver.find_elements_by_tag_name("a")
	for course in courses:
		print(course.text)
		if(course.text == to_find):
			course.click()
			return

	print("ERR: COURSE NOT FOUND")
	driver.quit()

def add_course_to_worklist():
	register_courses = input("Course(s): ")
	register_list = register_courses.split(", ")
	target_worklist = input("Worklist: ")

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

	for register in register_list:
		dept = register.split(" ")[0].upper()
		course = register.split(" ")[1]
		section = register.split(" ")[2]

		findLink(f"{dept}", driver)
		findLink(f"{dept} {course}", driver)
		findLink(f"{dept} {course} {section}", driver)

		#search for worklist
		get_active_el = driver.find_elements_by_xpath("//li[@class='active']")
		active_el = []
		for el in get_active_el:
			active_el.append(el.text)

		get_inactive_el = driver.find_elements_by_xpath("//li[not(@class='active')]")
		inactive_el = []
		for el in get_inactive_el:
			inactive_el.append(el.text)

		if(target_worklist in active_el):
			driver.find_element(By.PARTIAL_LINK_TEXT, 'Save To Worklist').click()
		elif(target_worklist in inactive_el):
			driver.find_element(By.PARTIAL_LINK_TEXT, f'{target_worklist}').click()
			driver.find_element(By.PARTIAL_LINK_TEXT, f'{dept} {course} {section}').click()
			driver.find_element(By.PARTIAL_LINK_TEXT, 'Save To Worklist').click()
		else:
			# create new worklist
			driver.find_element(By.PARTIAL_LINK_TEXT, 'New Worklist').click()
			driver.find_element_by_id("attrWorklistName").send_keys(target_worklist)
			driver.find_element_by_xpath("//input[@value='Create New Worklist']").click()
			driver.find_element(By.PARTIAL_LINK_TEXT, f'{dept} {course} {section}').click()
			driver.find_element(By.PARTIAL_LINK_TEXT, 'Save To Worklist').click()

		driver.find_element(By.PARTIAL_LINK_TEXT, 'Browse Courses').click()

	driver.quit()

# add_course_to_worklist()

