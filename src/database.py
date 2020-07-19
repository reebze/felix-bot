import sqlite3
db = sqlite3.connect('server.db')

class sql():
    
    def __init__(self):
        pass
        
    def commit(self):
        global db
        db.commit()
        
    def __enter__(self):
        global db
        self.sql_cursor = db.cursor()
        return self.sql_cursor
        
    def __exit__(self, type, value, traceback):
        global db
        self.sql_cursor.close()
        db.commit()