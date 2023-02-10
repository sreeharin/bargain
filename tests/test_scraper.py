import sys
import unittest
from random import choice

sys.path.append('../')
from scrapers import scraper 

class TestAmazonScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper.AmazonScraper()
        self.__fetch_data()

    def __fetch_data(self):
        data = self.scraper.fetch_data('ikigai')
        self.assertEqual(data.status_code, 200)
        with open('amazon_tmp.html', 'w') as amazon_tmp:
            amazon_tmp.write(data.text)

    def test_soup(self):
        with open('amazon_tmp.html', 'r') as amazon_data:
            soup = self.scraper.soup(amazon_data.read().strip()) 
            self.assertNotEqual(soup, None)
            self.assertEqual(
                    soup.title.string.split(':')[0].strip(), 'Amazon.in')

            items = soup.find_all(class_='sg-col-inner', limit=10)
            self.assertEqual(len(items), 10)

    def test_get_items(self):
        with open('amazon_tmp.html', 'r') as amazon_data:
            soup = self.scraper.soup(amazon_data.read().strip())
            items = self.scraper.get_items(soup)
            self.assertGreater(len(items), 0)
            for item in items:
                for value in item.get().values():
                    self.assertGreater(len(value), 0)

