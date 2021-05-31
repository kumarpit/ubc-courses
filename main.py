
# SEARCH FOR COURSE -> RETURNS ALL SECTIONS
# SEARCH FOR SECTIONS -> RETURNS AVAILABLE SEATS, TIMING, LINK TO REGISTER

from urllib.request import urlopen
from bs4 import BeautifulSoup

dept = input("Dept: ")
course = input("Course: ")

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

