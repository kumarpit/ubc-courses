from urllib.request import urlopen
from bs4 import BeautifulSoup

get_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=CPSC&course=210&section=921"

request_page = urlopen(get_url)
page_html = request_page.read()
request_page.close()

html_soup = BeautifulSoup(page_html, "html.parser")

seats = html_soup.find_all("strong") 

for seat in seats:
	print(seat)
