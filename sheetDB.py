import sqlite3

class sheetDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS sheet (reg text, operator text, odometer text, inspector text, makemodel text, date text, falselines text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM sheet")
        rows = self.cur.fetchall()
        return rows

    def insert(self, reg, operator, odometer, inspector, makemodel, date, falselines):
        self.cur.execute("INSERT INTO sheet VALUES (?, ?, ?, ?, ?, ?, ?)", (reg, operator, odometer, inspector, makemodel, date, falselines))
        self.conn.commit()