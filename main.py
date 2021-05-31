from urllib.request import urlopen
from bs4 import BeautifulSoup

dept = input("Dept: ")
course = input("Course: ")

get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept="+dept+"&course="+course

request_page = urlopen(get_url)
page_html = request_page.read()
request_page.close()

html_soup = BeautifulSoup(page_html, "html.parser")

sections = html_soup.find_all('td', class_=None) 

for section in sections:
	print(section.text)

# SEARCH FOR COURSE -> RETURNS ALL SECTIONS
# SEARCH FOR SECTIONS -> RETURNS AVAILABLE SEATS, TIMING, LINK TO REGISTER

