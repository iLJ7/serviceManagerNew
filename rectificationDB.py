import sqlite3

class rectificationDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS rectifications (reg text, checkno text, action text, rectifiedby text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM rectifications")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, reg, checkno, action, rectifiedby):
        self.cur.execute("INSERT INTO rectifications VALUES (?, ?, ?, ?)", (reg, checkno, action, rectifiedby))
        self.conn.commit()
    
    def remove(self, reg):
        self.cur.execute("DELETE FROM rectifications WHERE reg = ?", (reg,))
        self.conn.commit()
    
    #def updateDriver(self, reg, driver):
        #self.cur.execute("UPDATE trucks SET driver = ? WHERE reg = ?", (driver, reg))
        #self.conn.commit()
    
    #def updateColor(self, reg, color):
        #self.cur.execute("UPDATE trucks SET color = ? WHERE reg = ?", (color, reg))
        #self.conn.commit()

global rectDB
rectDB = rectificationDB('rectifications.db')
