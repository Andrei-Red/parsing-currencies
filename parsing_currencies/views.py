from django.shortcuts import render
from .parsing import record_db
import sqlite3
from datetime import datetime


#@cache_page(100)
def currencies(request):
    #record_db()
    content = get_currencies()
    last = len(content) - 26
    return render(request, 'base.html', {'content': content[last:]})


def get_currencies():
    date_now = str(datetime.now())[:10]
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f'SELECT country, unit, course, date FROM courses WHERE date LIKE "{date_now}%"')
    content = cursor.fetchall()
    conn.close()
    return content
