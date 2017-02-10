
import sqlite3 as lite
import sys

class DbHandler:

    def __init__(self, db):
        self.db = db
        self.cursor = self.connect()

    def connect(self):
        try:
            c = lite.connect(self.db)
            return  c.cursor()

        except lite.Error as e:
            raise e

    def execute(self, household, group):
        self.cursor.execute("SELECT BENEFIT FROM BENEFITS WHERE HOUSEHOLD=? AND CITY_GROUP=?", (household, group))
        return self.cursor.fetchone()[0]

    def get_benefit(self, household, group):

        if household <= 4:
            return self.execute(household, group)

        else:
            diff = household - 4
            benefit = self.execute(4, group)
            extra = self.execute(5, group)
            return benefit + diff*extra

    def find_city(self, city):

        self.cursor.execute("SELECT CITY_GROUP FROM CITIES WHERE NAME=?", (city, ))
        result = self.cursor.fetchone()

        if not result:
            return 4
        return result[0]

    def fetch_all(self, table):
        if table == "CITIES":
            self.cursor.execute("SELECT * FROM CITIES")
        else:
            self.cursor.execute("SELECT * FROM BENEFITS")
        return self.cursor.fetchall()
