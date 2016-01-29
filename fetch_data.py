import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime as dt

slug = "http://www.chucks85th.com"

r = requests.get(slug).content

conn = sqlite3.connect('chucks.db')
c = conn.cursor()

datetime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open('index.html', 'r') as r:
    soup = BeautifulSoup(r)

    lmenu = soup.findAll('li', {'class':['beer_even', 'beer_odd']})
    for beer in lmenu:
        info = beer.get_text()
        linelist = [x.strip() for x in info.split("\n")][1:7]
        linelist = [datetime] + linelist
        print linelist
        if linelist[2] != 'Growler':
            c.execute('INSERT INTO Beerlist VALUES (?,?,?,?,?,?,?)',
                    linelist)
conn.commit()
