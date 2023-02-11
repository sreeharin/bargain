import requests
import re
from urllib import parse
from bs4 import BeautifulSoup

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
        results_dict = {
                'name': self.name[0],
                'img': self.img[0],
                'price': self.price[0],
                'url': self.url,
                'reviews': self.reviews,
                'rating': self.rating,
                }
        return results_dict


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
            result_name = result.find(class_='a-text-normal').span.get_text()
            result_img = result.find(class_='s-image').get('src')
            result_price = result.find(class_='a-price-whole').get_text()
            # Some products may not have reviews or ratings
            try:
                result_rating = result.find(class_='a-icon-alt').string
            except AttributeError:
                result_rating = None
            try: 
                result_reviews = result.find(
                        class_='a-size-base s-underline-text').get_text()
            except AttributeError:
                result_reviews = None
            result_url = result.find(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').get('href')

            items.append(Result(result_name, result_img, 
                                result_price, result_reviews,
                                result_rating, result_url))

        return items


class FlipkartScraper(Scraper):
    def __init__(self):
        pass
