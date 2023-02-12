import re
from urllib import parse
from enum import IntFlag, auto
import logging
from bs4 import BeautifulSoup
import requests

logging.basicConfig(filename='scraper.log', encoding='utf-8',  
                    format="%(asctime)s [%(levelname)s]: %(message)s",
                    level=logging.DEBUG)

class Result:
    def __init__(self, name: str, img: str, 
                 price: str, reviews: str, 
                 rating: str, url: str):
        self.name = name,
        self.img = img,
        self.price= price,
        self.reviews = reviews
        self.rating = rating
        self.url = url

    def get(self) -> dict:
        # self.name, sef.img, self.price returns tuple hence `join` is used
        results_dict = {
                'name': self.name,
                'img': ''.join(self.img),
                'price': self.price,
                'reviews': self.reviews,
                'rating': self.rating,
                'url': self.url,
                }
        return results_dict

class FlipkartDivClass(IntFlag):
    '''Helper class for FlipkartScraper'''
    CLASS_1 = auto()
    CLASS_2 = auto()
    CLASS_3 = auto()


class Scraper:
    def __init__(self, url: str):
        self.url = url

    def fetch_data(self, query: str) -> requests.models.Response:
        logging.info(f'Fetching results for query: {query}')
        headers = {
                'Content-Type': 'text/*',
                'User-Agent': 'bargainer'
                }
        return requests.get(self.url+parse.quote_plus(query), headers=headers)

    def soup(self, data: str) -> BeautifulSoup:
        logging.info('Returning soup')
        return BeautifulSoup(data, 'html5lib')


class AmazonScraper(Scraper):
    def __init__(self):
        AMAZON_URL = 'https://www.amazon.in/s?k='
        super().__init__(AMAZON_URL)

    def get_items(self, soup: BeautifulSoup, limit: int = 10) -> list[Result]:
        '''Retrieve data from soup object'''
        logging.info('Returning results from Amazon')
        items = []
        search_results = soup.find_all(
                attrs={'data-component-type': 's-search-result'}, limit=limit)

        for result in search_results:
            result_name = result.find(
                    'span', class_='a-text-normal').string
            result_img = result.find(class_='s-image').get('src')
            result_price = result.find(
                    'span', class_='a-price-whole').string
            result_url = result.find(
                    class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
                    ).get('href')
            # Some products may not have reviews or ratings
            try:
                result_rating = result.find(class_='a-icon-alt').string
            except AttributeError:
                result_rating = None
                logging.error('No rating found for search query')
            try: 
                result_reviews = result.find(
                        class_='a-size-base s-underline-text'
                        ).get_text().strip('(').strip(')')
            except AttributeError:
                result_reviews = None
                logging.error('No reviews found for search query')

            items.append(Result(result_name, result_img, 
                                result_price, result_reviews,
                                result_rating, result_url))
        return items


class FlipkartScraper(Scraper):
    def __init__(self):
        FLIPKART_URL = 'https://www.flipkart.com/search?q='
        super().__init__(FLIPKART_URL)

    def get_items(self, soup: BeautifulSoup, limit: int = 10) -> list[Result]:
        logging.info('Returning results from Flipkart')
        items = []

        # Unlike Amazon.in Flipkart.com has more than one css class 
        # for showing results
        DIV_CLASS1 = '_1xHGtK _373qXS'
        DIV_CLASS2 = '_4ddWXP'
        DIV_CLASS3 = '_2kHMtA'

        div_class_dict = {
                DIV_CLASS1: FlipkartDivClass.CLASS_1,
                DIV_CLASS2: FlipkartDivClass.CLASS_2,
                DIV_CLASS3: FlipkartDivClass.CLASS_3,
                }

        # search_results = soup.find_all(class_=DIV_CLASS1, limit=limit)
        # if search_results == []:
        #     search_results = soup.find_all(class_=DIV_CLASS2, limit=limit)
        #     selected_class = FlipkartDivClass.CLASS_2

        for div_class in [DIV_CLASS1, DIV_CLASS2, DIV_CLASS3]:
            search_results = soup.find_all(class_=div_class, limit=limit)
            if search_results != []:
                selected_class = div_class_dict[div_class]
                logging.info(f'Selecting class: {div_class} for Flipkart')
                break
        
        ITEM_PRICE = '_30jeq3'
        match selected_class:
            case FlipkartDivClass.CLASS_1:
                # Generic items don't have reviews and rating
                ITEM_CLASS = 'IRpwTa' 
                ITEM_IMG = '_2r_T1I' 
                ITEM_REVIEWS = None
                ITEM_RATING = None
            case FlipkartDivClass.CLASS_2:
                ITEM_CLASS = 's1Q9rs'
                ITEM_IMG = '_396cs4'
                ITEM_REVIEWS = '_2_R_DZ'
                ITEM_RATING = '_3LWZlK'
            case FlipkartDivClass.CLASS_3:
                ITEM_PRICE = '_30jeq3 _1_WHN1'
                ITEM_IMG = '_396cs4'
                ITEM_REVIEWS = '_2_R_DZ'
                ITEM_RATING = '_3LWZlK'

        for result in search_results:
            if selected_class == FlipkartDivClass.CLASS_3:
                result_name = result.find('div', class_='_4rR01T').string
                result_url = result.find('a', class_='_1fQZEK').get('href')
            else:
                item = result.find('a', class_=ITEM_CLASS)
                result_name = item.get('title')
                result_url = item.get('href')
            result_img = result.find('img', class_=ITEM_IMG).get('src')
            result_price = result.find(class_=ITEM_PRICE).get_text()
            result_rating = None
            result_reviews = None
            if ITEM_RATING:
                try:
                    result_rating = result.find(
                            class_=ITEM_RATING).next_element
                except AttributeError:
                    logging.error('No rating found for search query')
                    continue

            if ITEM_REVIEWS:
                try:
                    result_reviews = result.find(
                            class_=ITEM_REVIEWS
                            ).get_text().strip('(').strip(')')
                except AttributeError:
                    logging.error('No reviews found for search query')
                    continue

            items.append(Result(result_name, result_img, 
                                result_price, result_reviews,
                                result_rating, result_url))
        return items

