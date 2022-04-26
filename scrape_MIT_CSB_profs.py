from email import header
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlsplit, urlunsplit

URL = "https://csbphd.mit.edu/faculty"
page = requests.get(URL)
split_url = urlsplit(URL)

net_loc = split_url.netloc
scheme = split_url.scheme

soup = BeautifulSoup(page.content, "html.parser")

profs = []
for profile in soup.find_all("td", class_="views-field-field-sort-name"):
    link = profile.find('a').get('href')
    profile_URL = scheme + "://" + net_loc + link
    profile_page = requests.get(profile_URL)
    profile_soup = BeautifulSoup(profile_page.content, "html.parser")

    name = profile_soup.find('h1', {"id": "page-title"}).string
    print(name)
    department_section = profile_soup.find('section', class_="field-name-field-department").find_all('li')
    department = ", ".join([x.string.strip() for x in department_section])
    print(department)

    external_links = profile_soup.find_all('a')
    lab_website = ""
    for l in external_links:
        if l.string == 'Lab Website':
            lab_website = l.get('href')

    email = profile_soup.find('div', class_="field-name-field-email").find('a').string
    office = profile_soup.find('section', class_="field-name-field-room").find('div', class_="field-item").string
    
    try:
        description_contents = profile_soup.find('section', class_="field-name-field-research-summary").find('p').contents
        description = ". ".join([x for x in description_contents if isinstance(x, str)])
    except AttributeError:
        description = ""

    print(description)
    profs.append([name, department, description, profile_URL, lab_website, email])
    

df = pd.DataFrame(profs, columns=["Name", "Department","Description", "Link", "Lab Website", "Email"])

df.to_csv("~/Desktop/MIT_CSB_profs.csv", index=False)
