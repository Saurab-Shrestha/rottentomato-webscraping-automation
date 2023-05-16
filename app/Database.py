import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

class SqliteDatabase:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.con = None
        self.cur = None

    def connect(self):
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()

    def create_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS movies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT NOT NULL,
                tomatometer_score TEXT,
                audience_score TEXT,
                tomatometer_state TEXT,
                storyline TEXT,
                rating TEXT,
                genres TEXT,
                review_1 TEXT,
                review_2 TEXT,
                review_3 TEXT,
                review_4 TEXT,
                review_5 TEXT,
                status TEXT
            )
        """
        self.cur.execute(create_table_sql)

    def insert_into_table(self, movie_data):
        if movie_data is None:
            logging.error("movie_data is None")
            return
        insert_sql = """
            INSERT INTO movies (
                movie_name, 
                tomatometer_score, 
                audience_score, 
                tomatometer_state, 
                storyline, 
                rating, 
                genres, 
                review_1, 
                review_2, 
                review_3, 
                review_4, 
                review_5, 
                status
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cur.execute(insert_sql, (
            movie_data["movie_name"],
            movie_data["tomatometer_score"],
            movie_data["audience_score"],
            movie_data["tomatometer_state"],
            movie_data["storyline"],
            movie_data["rating"],
            movie_data["genres"],
            movie_data["review_1"],
            movie_data["review_2"],
            movie_data["review_3"],
            movie_data["review_4"],
            movie_data["review_5"],
            movie_data["status"]
        ))
        self.con.commit()

    def close_db(self):
        self.cur.close()
        self.con.close()
        