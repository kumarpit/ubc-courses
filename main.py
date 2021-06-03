from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import pyperclip as pc

options = Options()
options.add_argument("--log-level=3")
global DRIVER_PATH
DRIVER_PATH = "C:/Users/Lenovo/Downloads/chromedriver_win32/chromedriver"

def scrape(url):
	request_page = urlopen(url)
	page_html = request_page.read()
	request_page.close()
	return page_html

def printTable(table):
	for tr in table:
		td = tr.find_all("td")
		row = [i.text for i in td]
		print(row)

def getCourses(dept):
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-department&dept="+dept
	page_html = scrape(get_url)
	html_soup = BeautifulSoup(page_html, "html.parser")
	table = html_soup.find("table", id="mainTable")
	try:
		printTable(table.find_all("tr"))
	except:
		print("INVALID")
	start()

def getSections(dept, course):
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept="+dept+"&course="+course
	page_html = scrape(get_url)
	html_soup = BeautifulSoup(page_html, "html.parser")
	table = html_soup.find("table", class_="section-summary")
	try:
		for to_delete in table.find_all("td", class_="section-comments"):
			to_delete.decompose()
		printTable(table.find_all("tr"))
	except:
		print("INVALID")
	start()

def getProf(prof):
	name = prof.split(" ")
	prof_url = "https://www.ratemyprofessors.com/search/teachers?query=" + name[1].replace(",", "") + "+" + name[0].replace(",", "")
	search_prof = input("View Prof? ")
	if(search_prof == ""):
		return
	else:
		driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
		driver.get(prof_url)
		driver.find_element_by_css_selector('[alt="Banner Close Icon"]').click()

def getSeats(dept, course, section):
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept="+dept+"&course="+course+"&section="+section
	page_html = scrape(get_url)
	html_soup = BeautifulSoup(page_html, "html.parser")
	seat_sum = html_soup.find("table", class_="'table")
	table_el = html_soup.find_all("td")
	td_link = []

	try:
		printTable(seat_sum.find_all("tr"))
		for td in table_el:
			if td.find_all("a") != []:
				td_link.append(td)
		pc.copy(get_url)
		
		for link in td_link:
				print(f"Instructor: {link.text}")
		
		print("Registration link copied to clipboard")
		getProf(td_link[0].text)
	except:
		print("INVALID")
	start()

def getAll():
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea"
	page_html = scrape(get_url)
	html_soup = BeautifulSoup(page_html, "html.parser")
	table = html_soup.find("table", id="mainTable")
	printTable(table.find_all("tr"))
	print("* indicates no courses offered for current term")
	start()

def getCurrTerm():
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea"
	page_html = scrape(get_url)
	html_soup = BeautifulSoup(page_html, "html.parser")
	buttons = html_soup.find_all("button", class_="btn-primary")

	for bt in buttons:
		print(bt.text)

def start():
	dept = input("Dept: ").replace(" ", "")

	if(dept == "-1"):
		sys.exit()	
	elif(dept == "all"):
		getAll()
		return
	
	course = input("Course: ").replace(" ", "")

	if(len(course) == 0):
		getCourses(dept)
		return
	else:
		section = input("Section: ").replace(" ", "")
	
	if(len(section) == 0):
		getSections(dept, course)
	else:
		getSeats(dept, course, section)
			
getCurrTerm()
start()
