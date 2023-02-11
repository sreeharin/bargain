import re
from urllib import parse
from enum import IntFlag, auto
from bs4 import BeautifulSoup
import requests

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
                'name': ''.join(self.name),
                'img': ''.join(self.img),
                'price': ''.join(self.price),
                'reviews': self.reviews,
                'rating': self.rating,
                'url': self.url,
                }
        return results_dict

class FlipkartDivClass(IntFlag):
    '''Helper class for FlipkartScraper'''
    CLASS_1 = auto()
    CLASS_2 = auto()


class Scraper:
    def __init__(self, url: str):
        self.url = url

    def fetch_data(self, query: str) -> requests.models.Response:
        headers = {
                'Content-Type': 'text/*',
                'User-Agent': 'bargainer'
                }
        return requests.get(self.url+parse.quote_plus(query), headers=headers)

    def soup(self, data: str) -> BeautifulSoup:
        return BeautifulSoup(data, 'html5lib')


class AmazonScraper(Scraper):
    def __init__(self):
        AMAZON_URL = 'https://www.amazon.in/s?k='
        super().__init__(AMAZON_URL)

    def get_items(self, soup: BeautifulSoup, limit: int = 10) -> list[Result]:
        '''Retrieve data from soup object'''
        items = []
        search_results = soup.find_all(
                attrs={'data-component-type': 's-search-result'}, limit=limit)

        for result in search_results:
            result_name = result.find(
                    'span', class_='a-text-normal').get_text()
            result_img = result.find(class_='s-image').get('src')
            result_price = result.find(class_='a-price-whole').get_text()
            result_url = result.find(
                    class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
                    ).get('href')
            # Some products may not have reviews or ratings
            try:
                result_rating = result.find(class_='a-icon-alt').string
            except AttributeError:
                result_rating = None
            try: 
                result_reviews = result.find(
                        class_='a-size-base s-underline-text'
                        ).get_text().strip('(').strip(')')
            except AttributeError:
                result_reviews = None

            items.append(Result(result_name, result_img, 
                                result_price, result_reviews,
                                result_rating, result_url))
        return items


class FlipkartScraper(Scraper):
    def __init__(self):
        FLIPKART_URL = 'https://www.flipkart.com/search?q='
        super().__init__(FLIPKART_URL)

    def get_items(self, soup: BeautifulSoup, limit: int = 10) -> list[Result]:
        items = []

        # Unlike Amazon.in Flipkart.com has two css classes for showing results
        # DIV_CLASS1 doesn't contain ratings and reviews
        DIV_CLASS1 = '_1xHGtK _373qXS'
        DIV_CLASS2 = '_4ddWXP'
        selected_class = FlipkartDivClass.CLASS_1

        search_results = soup.find_all(class_=DIV_CLASS1, limit=limit)
        if search_results == []:
            search_results = soup.find_all(class_=DIV_CLASS2, limit=limit)
            selected_class = FlipkartDivClass.CLASS_2
        
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

        for result in search_results:
            item = result.find('a', class_=ITEM_CLASS)
            result_name = item.get('title')
            result_img = result.find('img', class_=ITEM_IMG).get('src')
            result_price = result.find(class_=ITEM_PRICE).get_text()
            result_url = item.get('href')
            result_rating = None
            result_reviews = None
            if ITEM_RATING:
                try:
                    result_rating = result.find(
                            class_=ITEM_RATING).next_element
                except AttributeError:
                    continue

            if ITEM_REVIEWS:
                try:
                    result_reviews = result.find(
                            class_=ITEM_REVIEWS
                            ).get_text().strip('(').strip(')')
                except AttributeError:
                    continue

            items.append(Result(result_name, result_img, 
                                result_price, result_reviews,
                                result_rating, result_url))
        return items

