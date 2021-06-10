from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from script import add_course_to_worklist, pre_add_to_list
import sys
import pyperclip as pc
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

options = Options()
options.add_argument("--log-level=3")
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
		print(Fore.RED + "INVALID")
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
		print(Fore.RED + "INVALID")
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
		print("Registration link copied to clipboard")
		
		for link in td_link:
				if "," in link.text:
					print(f"Instructor: {link.text}")
					getProf(link.text)
					break
	except:
		print(Fore.RED + "INVALID")
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
		print(Style.BRIGHT + bt.text)

def start():
	dept = input("Dept: ").replace(" ", "")

	if(dept == "-1"):
		sys.exit()	
	elif(dept == "all"):
		return getAll()
	elif(dept == "register"):
		add_course_to_worklist()
		return start()
	elif(dept == "add"):
		pre_add_to_list()
		return start()
	
	course = input("Course: ").replace(" ", "")

	if(len(course) == 0):
		return getCourses(dept)
	else:
		section = input("Section: ").replace(" ", "")
	
	if(len(section) == 0):
		getSections(dept, course)
	else:
		getSeats(dept, course, section)
			
getCurrTerm()
start()
