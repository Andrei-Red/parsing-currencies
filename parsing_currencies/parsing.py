import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime


url = 'https://www.nbrb.by/statistics/rates/ratesdaily.asp'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', 'accept': '*/*'}


def create_table_db():
    conn = sqlite3.connect('db.sqlite3')
    sql = 'CREATE TABLE courses (country TEXT, unit TEXT, course TEXT, date TEXT)'
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.close()


def pars(url, headers):
    source = requests.get(url, headers)
    pars_html = source.text
    text_content = BeautifulSoup(pars_html, 'html.parser')
    table_elem = text_content.find_all('tr')

    content = []
    for item in table_elem:
        if item.find('span', class_="text"):
            country = (item.find('span', class_="text").get_text())
            unit = (item.find('td', class_="curAmount").get_text())
            course = (item.find('td', class_="curCours").get_text()[1:])
            date = str(datetime.now())

            content.append((country, unit, course, date))
    return content


def record():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    query = "INSERT INTO courses VALUES (?, ?, ?, ?)"

    content = pars(url, headers)
    for item in content:
        cursor.execute(query, item)
    conn.commit()
    conn.close()


def record_db():
    try:
        create_table_db()
    except:
        pass
    record()

