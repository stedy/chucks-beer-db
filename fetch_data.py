import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime as dt

slug = "http://www.chucks85th.com"

opening = dt.datetime.combine(dt.datetime.today(), dt.time(11,0,0))
closing = dt.datetime.combine(dt.datetime.today(), dt.time(23,59,0))

if opening < dt.datetime.now() < closing:
    r = requests.get(slug).content

    conn = sqlite3.connect('chucks.db')
    c = conn.cursor()

    datetime_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    soup = BeautifulSoup(r)

    lmenu = soup.findAll('li', {'class':['beer_even', 'beer_odd']})
    for beer in lmenu:
        info = beer.get_text()
        linelist = [datetime_str] + [x.strip() for x in info.split("\n")][1:7]
        if linelist[2] != 'Growler':
            c.execute('INSERT INTO Beerlist VALUES (?,?,?,?,?,?,?)',
                    linelist)
    conn.commit()
