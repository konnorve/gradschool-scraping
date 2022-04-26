from email import header
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlsplit, urlunsplit

URL = "https://be.mit.edu/research/faculty"
page = requests.get(URL)
split_url = urlsplit(URL)

net_loc = split_url.netloc
scheme = split_url.scheme

soup = BeautifulSoup(page.content, "html.parser")

profs = []
for profile in soup.find_all("div", class_="views-field views-field-title"):
    name = profile.find('a').string.split(',')[0]
    print(name)
    link = profile.find('a').get('href')
    profile_URL = scheme + "://" + net_loc + link
    profile_page = requests.get(profile_URL)

    profile_soup = BeautifulSoup(profile_page.content, "html.parser")

    lab_website_section = profile_soup.find('section', class_="field-name-field-faculty-lab-website")
    try:
        lab_website = lab_website_section.find('a').get('href')
    except AttributeError:
        lab_website = ""

    email = profile_soup.find('section', class_="field-name-field-faculty-email-address").find('a').string
    office = profile_soup.find('section', class_="field-name-field-faculty-office").find('a').string
    
    description_contents = profile_soup.find('section', class_="field-name-field-faculyt-research").find('p').contents
    description = ". ".join([x for x in description_contents if isinstance(x, str)])
    
    profs.append([name, description, profile_URL, lab_website, email])

df = pd.DataFrame(profs, columns=["Name", "Description", "Link", "Lab Website", "Email"])

df.to_csv("~/Desktop/MIT_bioE_profs.csv", index=False)