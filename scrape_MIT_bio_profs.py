from email import header
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://biology.mit.edu/faculty-and-research/faculty/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

profs = []
for profile in soup.find_all("div", class_="profile-item"):
    first_name = profile.find('span', class_='first-name').string
    last_name = profile.find('span', class_='last-name').string
    description = profile.find('p', class_='profile-description').string
    link = profile.find('a', attrs={'href': re.compile("^https://")}).get('href')
    profs.append([f"{first_name} {last_name}", description, link])

df = pd.DataFrame(profs, columns=["Name", "Description", "Link"])

df.to_csv("MIT_bio_profs.csv", index=False)