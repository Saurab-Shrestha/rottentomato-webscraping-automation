import logging
from app.Database import SqliteDatabase
from app.Excel import ExcelRead
from app.Browser import RottenTomatoesScraper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

class MovieScraper:
    def __init__(self, db_name, excel_file):
        self.db = SqliteDatabase(db_name)
        self.excel = ExcelRead(excel_file)
        self.scrapper = RottenTomatoesScraper()

    def create_database_connection(self):
        self.db.connect()

    def create_database_table(self):
        try:
            self.db.create_table()
        except Exception as e:
            logging.info("Database:", e)

    def read_from_excel(self):
        try:
            worksheet = self.excel.read_excel()
        except:
            logging.info("Unable to read from excel.")
        return worksheet
    
    def scrape_movies_and_insert_into_db(self,worksheet):
        try:
            self.scrapper.open_rotten_tomatoes_website()
            for movie in worksheet:
                logging.info(movie['Movie'])
                movie_name = str(movie['Movie'])
                if movie_name == "":
                    break

                self.scrapper.search_movie(movie_name)
                self.scrapper.filter_movie()
                link, movie = self.scrapper.locate_exact_movie(movie_name)
                movie_data = self.scrapper.extract_movie_data(link, movie)
                logging.info(movie_data)
                self.db.insert_into_table(movie_data)
        except:
            logging.info("Unable to extract data!")


    def close_connections(self):
        self.db.close_db()
        self.scrapper.close_browser()


def main():
    db_name = "rotten.db"
    excel_file = "movies.xlsx"
    
    scraper = MovieScraper(db_name, excel_file)
    scraper.create_database_connection()
    scraper.create_database_table()
    worksheet = scraper.read_from_excel()
    scraper.scrape_movies_and_insert_into_db(worksheet)
    scraper.close_connections()


if __name__ == "__main__":
    main()
