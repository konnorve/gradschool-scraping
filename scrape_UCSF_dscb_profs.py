from email import header
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlsplit, urlunsplit

URL = "https://tetrad.ucsf.edu/faculty"

faculty_profiles = []

page = requests.get(URL)
split_url = urlsplit(URL)

net_loc = split_url.netloc
scheme = split_url.scheme

soup = BeautifulSoup(page.content, "html.parser")

profs = []
for block in soup.find_all("div", class_="views-row"):

    name = block.find("h2").find("a").contents[0]

    department = 

    program = "Developmental & Stem Cell Biology"

    try:
        description = block.find("div", class_="field-name-field-research-title").div.div.string
    except AttributeError:
        description = None

    profile_URL = block.find("h2").find("a").get('href')

    try:
        lab_website = block.find("div", class_="field-name-field-lab-website").find("a").get('href')
    except AttributeError:
        lab_website = None


    email = None

    for x in [name, department, description, profile_URL, lab_website, email]:
        print(x)
    print()
    print()

    profs.append([name, department, program, description, profile_URL, lab_website, email])

df = pd.DataFrame(profs, columns=["Name", "Department", "Program", "Description", "Link", "Lab Website", "Email"])

df.to_csv("UCSF_Tetrad_profs.csv", index=False)