import requests
from urllib import parse
from bs4 import BeautifulSoup

class Result:
    def __init__(self, name, img, price, url):
        self.name = name,
        self.img = img,
        self.price = price,
        self.url = url


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

    def get_items(self, soup: BeautifulSoup, limit: int = 10) -> list:
        items = []
        DIV_CLASS = 's-card-container s-overflow-hidden aok-relative puis-expand-height puis-include-content-margin puis s-latency-cf-section s-card-border'
        arr = soup.find_all(class_=DIV_CLASS, limit=limit) 

        for item in arr:
            name = item.find(class_='a-size-base-plus a-color-base a-text-normal')
            price = item.find(class_='a-price-whole')
            img = item.find(class_='s-image')
            if name and price and img:
                result_name = name.string
                result_price = price.get_text().strip('.')
                result_img = img.get('src')
                result_url = item.a.get('href')

                items.append(
                        Result(result_name, result_img, 
                               result_price, result_url)
                        )
        return items


class FlipkartScraper(Scraper):
    def __init__(self):
        pass
