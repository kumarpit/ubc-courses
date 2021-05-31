# SEARCH FOR SUBJECT -> RETURN ALL COURSES
# SEARCH FOR COURSE -> RETURNS ALL SECTIONS
# SEARCH FOR SECTIONS -> RETURNS AVAILABLE SEATS, TIMING, LINK TO REGISTER

from urllib.request import urlopen
from bs4 import BeautifulSoup

dept = input("Dept: ")
course = input("Course: ")

def getCourses():
	request_page = urlopen(get_url)
	page_html = request_page.read()
	request_page.close()

	html_soup = BeautifulSoup(page_html, "html.parser")

	table = html_soup.find("table", id="mainTable")

	for tr in table.find_all("tr"):
		td = tr.find_all("td")
		row = [i.text for i in td]
		print(row)

def getSections():
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

if(len(course) == 0):
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-department&dept="+dept
	getCourses()
else:
	get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept="+dept+"&course="+course
	getSections()
