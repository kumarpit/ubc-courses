from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)

DRIVER_PATH = "C:/Users/Lenovo/Downloads/chromedriver_win32/chromedriver"

options = Options()
options.headless = False
options.add_argument("--window-size=1500,1200")
options.add_argument("--log-level=3")

USER = os.environ['USER']
PASS = os.environ['PASS']

courseList = []

def pre_add_to_list():
	for course in input("Add courses: ").split(", "):
		courseList.append(course)

def findLink(to_find, selector):
	courses = driver.find_elements_by_css_selector(selector)
	for course in courses:
		if(course.text == to_find):
			print(Back.GREEN + course.text)
			course.click()
			return True
		else:
			print(course.text)

	print(Fore.RED + f"ERR: {to_find} NOT FOUND")
	driver.find_element(By.PARTIAL_LINK_TEXT, 'Browse Courses').click()
	return False

#created only because I was tired of deleting all worklists I made while testing  manually
# def delete_worklists():
# 	driver.find_element(By.PARTIAL_LINK_TEXT, 'Browse Courses').click()

def add_course_to_worklist():
	register_courses = input("Course(s): ")
	register_list = register_courses.split(", ")
	
	for pre_saved in courseList:
		register_list.append(pre_saved)

	for courses in register_list:
		print(Fore.YELLOW + courses)

	target_worklist = input("Worklist: ")

	global driver
	driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
	driver.get("https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments")
	driver.find_element_by_xpath("//input[@type='IMAGE']").click()
	driver.find_element_by_id("username").send_keys(USER)
	driver.find_element_by_id("password").send_keys(PASS)
	driver.find_element_by_xpath("//input[@type='submit']").click()

	print(Fore.YELLOW + "LOGGING IN...")

	timeout = 10

	try:
		element_present = EC.presence_of_element_located((By.ID, 'mainTable'))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print(Fore.RED + "TIMEOUT")

	for register in register_list:
		dept = register.split(" ")[0].upper()
		course = register.split(" ")[1]
		section = register.split(" ")[2]

		print(Fore.YELLOW + "FINDING COURSE...")

		if(not(findLink(f"{dept}", "table[id='mainTable'] a")) or
		 not(findLink(f"{dept} {course}", "table[id='mainTable'] a")) or 
		 not(findLink(f"{dept} {course} {section}", "table[class='table table-striped section-summary'] a"))):
			continue

		print(Fore.YELLOW + "SAVING TO WORKLIST...")

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
			print(Fore.GREEN + "SAVED TO WORKLIST")
		elif(target_worklist in inactive_el):
			driver.find_element(By.PARTIAL_LINK_TEXT, f'{target_worklist}').click()
			driver.find_element(By.PARTIAL_LINK_TEXT, f'{dept} {course} {section}').click()
			driver.find_element(By.PARTIAL_LINK_TEXT, 'Save To Worklist').click()
			print(Fore.GREEN + "SAVED TO WORKLIST")
		else:
			# create new worklist
			driver.find_element(By.PARTIAL_LINK_TEXT, 'New Worklist').click()
			driver.find_element_by_id("attrWorklistName").send_keys(target_worklist)
			driver.find_element_by_xpath("//input[@value='Create New Worklist']").click()
			driver.find_element(By.PARTIAL_LINK_TEXT, f'{dept} {course} {section}').click()
			driver.find_element(By.PARTIAL_LINK_TEXT, 'Save To Worklist').click()
			print(Fore.GREEN + "WORKLIST CREATED")
			print(Fore.GREEN + "SAVED TO WORKLIST")

		driver.find_element(By.PARTIAL_LINK_TEXT, 'Browse Courses').click()

	driver.close()



