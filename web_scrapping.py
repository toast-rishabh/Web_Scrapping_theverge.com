from bs4 import BeautifulSoup
import requests
import csv
import datetime
import sqlite3
import pandas as pd

#Defining Page for Scraping
page = requests.get("https://theverge.com")
soup = BeautifulSoup(page.content, "html.parser")

#Getting Date to use as CSV filename
date = datetime.datetime.now()
file = date.strftime('%d%m%Y_verge.csv')

#Header for our CSV file
header = ['ID', 'URL', 'Headline', 'Author', 'Date/Time']
with open(file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

#Getting All Articles
all_link = soup.find_all("a", {"data-chorus-optimize-field": "hed"})

id=1
#Loop for Getting Each Article, Extracting URL, Author Name and Date and then Writing the data into CSV file.
for link in all_link:
    name = []
    try:
        ind_page = requests.get(link.get('href'))
    except requests.exceptions.ReadTimeout:
        print("Request Timeout")
    ind_soup = BeautifulSoup(ind_page.content, "html.parser")
    time = ind_soup.find("time",{"class": "c-byline__item"})
    author_name = ind_soup.find_all("span",{"class": "c-byline__author-name"})
    for text in author_name:
        name.append(text.text)
    author = ', '.join(name)
    data = [id,link.get('href'),link.text.strip(),author,time.text.strip()]
    with open(file, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    id = id+1

#Saving the data in SQLite Database
conn = sqlite3.connect('theverge.db')
stud_data = pd.read_csv(file)
stud_data.to_sql(file, conn, if_exists='replace', index=False)
conn.close()