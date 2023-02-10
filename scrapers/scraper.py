import requests
import re
from urllib import parse
from bs4 import BeautifulSoup

class Result:
    def __init__(self, name: str, img: str, 
                 price: str, url: str, 
                 reviews: str, rating: str):
        self.name = name,
        self.img = img,
        self.price= price,
        self.url = url
        self.reviews = reviews
        self.rating = rating

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

    def get_items(self, soup: BeautifulSoup, limit: int = 1) -> list[Result]:
        items = []
        DIV_CLASS = 'sg-col-inner'
        arr = soup.find_all(class_=DIV_CLASS, limit=limit) 
        print(arr)

        for item in arr:
            name = item.find(class_='a-size-base-plus a-color-base a-text-normal')
            price = item.find(class_='a-price-whole')
            img = item.find(class_='s-image')
            reviews = item.find(class_='a-size-base s-underline-text')
            rating_div = item.find(class_='a-icon-alt')
            if name and price and img and reviews and rating_div:
                result_name = name.string
                result_price = price.get_text().strip('.')
                result_img = img.get('src')
                result_url = item.a.get('href')
                result_reviews = reviews.string
                result_rating = rating_div.string.split(' ')[0]

                items.append(
                        Result(result_name, result_img, 
                               result_price, result_url,
                               result_reviews, result_rating)
                        )
        return items


class FlipkartScraper(Scraper):
    def __init__(self):
        pass
