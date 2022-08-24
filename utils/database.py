#!/usr/bin/env python3
#-*- coding:utf -8-*-

from config import Config
import sqlite3, time, logging, os


r = '\033[31m'
e = '\033[0m'
y = '\033[33m'


class Database:
    if not os.path.exists(Config.DATABASE_PATH):
        logging.info(f'\n{y}[ ! ]{e} Database file not found. Creating new one...\n')
    
    def __init__(self):
        self.conn = sqlite3.connect(Config.DATABASE_PATH)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS posts (id TEXT, url TEXT, added_date FLOAT)")
        self.conn.commit()

    def insert(self, id, url):
        if self.search(id=id) == []:
            self.cur.execute("INSERT INTO posts VALUES (?, ?, ?)", (id, url, time.time()))
            self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM posts")
        rows = self.cur.fetchall()
        return rows

    def search(self, id='', url=''):
        self.cur.execute("SELECT * FROM posts WHERE url=? OR id=?", (url, id))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM posts WHERE id=?", (id))
        self.conn.commit()

    def update(self, id, url):
        self.cur.execute("UPDATE posts SET url=? WHERE id=?", (url, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


