import logging
from time import sleep
from RPA.Browser.Selenium import Selenium


URL = "https://www.rottentomatoes.com/"
BROWSER = "firefox"

SEARCH_BAR = "//input[@data-qa='search-input']"
SEARCH_INPUT = '//*[@id="header-main"]/search-algolia/search-algolia-controls/input'
SEARCH_CLICK = '//*[@id="header-main"]/search-algolia/search-algolia-controls/a'

MOVIE_FILTER = '//li[@data-filter="movie"]'
MOVIE_TITLE_LIST = '//ul[@slot="list"]/search-page-media-row/a[@data-qa="info-name"]'


class RottenTomatoesScraper:
    def __init__(self) -> None:
        self.browser_lib = Selenium(auto_close=False)

    def open_rotten_tomatoes_website(self):
        try:
            self.browser_lib.open_browser(URL,BROWSER)
            self.browser_lib.maximize_browser_window()
        except Exception:
            logging.info("Unable to open the browser!")
     
    def search_movie(self,movie_name):
        try:
            self.browser_lib.wait_until_element_is_visible(SEARCH_BAR,timeout=30)
            self.browser_lib.input_text(SEARCH_INPUT,movie_name)
            sleep(5)
            self.browser_lib.click_link(SEARCH_CLICK)
        except:
            logging.info("Unable to locate search input!")

    def filter_movie(self):
        try:
            self.browser_lib.wait_until_element_is_visible(MOVIE_FILTER)
            movie_filter = self.browser_lib.get_webelements(MOVIE_FILTER)
            self.browser_lib.click_element(movie_filter)
            sleep(5)
        except Exception:
            logging.info("Movie filter not found!")

    def locate_exact_movie(self, movie):
        given_movie = movie.strip()
        self.browser_lib.wait_until_page_contains_element(MOVIE_TITLE_LIST)
        titles = self.browser_lib.get_webelements(MOVIE_TITLE_LIST)

        latest_movie_title = None
        for title in titles:
            movie_title = self.browser_lib.get_text(title)
            movie_title_new = movie_title
            if movie_title_new == given_movie:
                latest_movie_title = movie_title
                link = self.browser_lib.get_element_attribute(title,'href')
                logging.info(link)
                logging.info(latest_movie_title)
                break
        
        # Extract data if movie found
        if latest_movie_title:
            return link, movie
        else:
            return None, movie

    def extract_movie_data(self,link, movie):
        if link:
            # Navigate to movie page
            try:
                self.browser_lib.go_to(link)
                sleep(5)
                movie_name = self.browser_lib.get_text("//h1[@class='title']")
                tomatometer_score = self.browser_lib.get_element_attribute('//score-board[@data-qa="score-panel"]', 'tomatometerscore')
                tomatometer_score = tomatometer_score if len(str(tomatometer_score)) > 0 else "N/A"

                audience_score = self.browser_lib.get_element_attribute('//score-board[@data-qa="score-panel"]', 'audiencescore')
                audience_score = audience_score if len(str(audience_score)) > 0 else "N/A"

                rating = self.browser_lib.get_element_attribute('//score-board[@data-qa="score-panel"]', 'rating')
                rating = rating if len(str(rating)) > 0 else "N/A"

                tomatometer_state = self.browser_lib.get_element_attribute('//score-board[@data-qa="score-panel"]', 'tomatometerstate')
                tomatometer_state = tomatometer_state if len(str(tomatometer_state)) > 0 else "N/A"

                self.browser_lib.wait_until_element_is_visible('id:movie-info')
                storyline = self.browser_lib.get_text('//p[@data-qa="movie-info-synopsis"]')
                genres = self.browser_lib.get_text('//*[@id="info"]/li[1]/p/span')

                self.browser_lib.wait_until_element_is_visible('id:critics-reviews')
                reviews = self.browser_lib.find_elements('//review-speech-balloon[@data-qa="critic-review"]')
                review_1 = reviews[0].text if len(reviews) >= 1 else "N/A"
                review_2 = reviews[1].text if len(reviews) >= 2 else "N/A"
                review_3 = reviews[2].text if len(reviews) >= 3 else "N/A"
                review_4 = reviews[3].text if len(reviews) >= 4 else "N/A"
                review_5 = reviews[4].text if len(reviews) >= 5 else "N/A"

                status = "Success"
                
                movie_data = {
                    "movie_name": movie_name,
                    "tomatometer_score": tomatometer_score,
                    "audience_score": audience_score,
                    "tomatometer_state": tomatometer_state,
                    "storyline": storyline,
                    "rating": rating,
                    "genres": genres,
                    "review_1": review_1,
                    "review_2": review_2,
                    "review_3": review_3,
                    "review_4": review_4,
                    "review_5": review_5,
                    "status": status
                }
                logging.info(movie_data)
                return movie_data
            except Exception as e:
                logging.info("Error: ",e)

        else:
            movie_data = {
                "movie_name": movie,
                "tomatometer_score": "N/A",
                "audience_score": "N/A",
                "tomatometer_state": "N/A",
                "storyline": "N/A",
                "rating": "N/A",
                "genres": "N/A",
                "review_1": "N/A",
                "review_2": "N/A",
                "review_3": "N/A",
                "review_4": "N/A",
                "review_5": "N/A",
                "status": "No exact match found"
            }
            return movie_data
        
    def close_browser(self):
        self.browser_lib.close_browser()