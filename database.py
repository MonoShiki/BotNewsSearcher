import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS i_post(href TEXT NOT NULL,information TEXT NOT NULL,img TEXT NOT NULL,date TEXT NOT NULL)')



    def add_post(self, href, information, img, date):
        with self.connection:
            return self.cursor.execute('INSERT INTO i_post VALUES(?,?,?,?)', (href, information, img, date))

    def get_all_posts(self):
        with self.connection:
            result = self.cursor.execute("SELECT href FROM i_post").fetchall()
            return [el[0] for el in result]
