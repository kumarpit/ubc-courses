# SEARCH FOR SUBJECT -> RETURN ALL COURSES
# SEARCH FOR COURSE -> RETURNS ALL SECTIONS
# SEARCH FOR SECTIONS -> RETURNS AVAILABLE SEATS, TIMING, LINK TO REGISTER

from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import pyperclip as pc

def getCourses(dept):
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-department&dept="+dept
	request_page = urlopen(get_url)
	page_html = request_page.read()
	request_page.close()
	html_soup = BeautifulSoup(page_html, "html.parser")

	table = html_soup.find("table", id="mainTable")

	for tr in table.find_all("tr"):
		td = tr.find_all("td")
		row = [i.text for i in td]
		print(row)

	start()

def getSections(dept, course):
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept="+dept+"&course="+course
	request_page = urlopen(get_url)
	page_html = request_page.read()
	request_page.close()
	html_soup = BeautifulSoup(page_html, "html.parser")

	table = html_soup.find("table", class_="section-summary")

	for to_delete in table.find_all("td", class_="section-comments"):
		to_delete.decompose()

	for tr in table.find_all("tr"):
		td = tr.find_all("td")
		row = [i.text for i in td]
		print(row)

	start()

def getSeats(dept, course, section):
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept="+dept+"&course="+course+"&section="+section
	request_page = urlopen(get_url)
	page_html = request_page.read()
	request_page.close()
	html_soup = BeautifulSoup(page_html, "html.parser")

	strong_el = html_soup.find_all("strong")
	for el in strong_el:
		print(el.text)
		
	pc.copy(get_url)
	print("Link copied to clipboard")

	start()

def start():
	dept = input("Dept: ")
	
	if(dept == "-1"):
		sys.exit()	

	course = input("Course: ")
	section = input("Section: ")

	if(len(course) == 0):
		getCourses(dept)
	elif(len(section) == 0):
		getSections(dept, course)
	else:
		getSeats(dept, course, section)

start()
