import pymysql
import os


class Database():

    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            db='capston',
            charset='utf8',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
