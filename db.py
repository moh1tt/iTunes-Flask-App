import sqlite3
import random
import datetime
from models import iTunes


def getNewId():
    return random.getrandbits(28)


music_starter_pack = [
    {
        'title': 'The Beatles',
        'artist': 'The Beatles',
        'price': 19.99,
        'album': 'The White Album'

    },
    {
        'title': 'The Boulevard of Broken Dreams',
        'artist': 'Green Day',
        'price': 1.99,
        'album': 'American Idiot'
    },
    {
        'title': 'Stairway to Heaven',
        'artist': 'Led Zeppelin',
        'price': 1.99,
        'album': 'Led Zeppelin IV'
    },
    {
        'title': 'Smells Like Teen Spirit',
        'artist': 'Nirvana',
        'price': 1.99,
        'album': 'Nevermind'
    },
    {
        'title': 'Hotel California',
        'artist': 'Eagles',
        'price': 1.99,
        'album': 'Hotel California'
    },

]


def connect():
    conn = sqlite3.connect('iTunes.db')
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS itunes (id INTEGER PRIMARY KEY, artist TEXT, title TEXT, price REAL, album TEXT)")
    conn.commit()
    conn.close()
    for i in music_starter_pack:
        m = iTunes(getNewId(), i['artist'], i['title'], i['price'], i['album'])
        insert(m)


def insert(music):
    conn = sqlite3.connect('iTunes.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO itunes VALUES (?,?,?,?,?)", (
        music.id, music.artist, music.title, music.price, music.album))
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect('itunes.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM itunes")
    rows = cur.fetchall()
    all_music = []
    for i in rows:
        music = iTunes(i[0], i[1], i[2], i[3], i[4])
        all_music.append(music)
    conn.close()
    return all_music


def update(music):
    conn = sqlite3.connect('iTunes.db')
    cur = conn.cursor()
    cur.execute("UPDATE itunes SET artist=?, title=?, price=?, album=? WHERE id=?", (
        music.artist, music.title, music.price, music.album, music.id))
    conn.commit()
    conn.close()


def delete(id):
    conn = sqlite3.connect('iTunes.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM itunes WHERE id=?", (id,))
    conn.commit()
    conn.close()


def deleteAll():
    conn = sqlite3.connect('iTunes.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM itunes")
    conn.commit()
    conn.close()
