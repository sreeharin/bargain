import sys
import unittest
from random import choice

sys.path.append('../')
from scraper import scraper 

class TestAmazonScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper.AmazonScraper()
        self.query = choice(
                ['trading books', 'men sunglasses', 
                 'casio watches for men', 'the alchemist',
                 'iphone', 'samsung watches'])
        self.__fetch_data()

    def __fetch_data(self):
        data = self.scraper.fetch_data(self.query)
        self.assertEqual(data.status_code, 200)
        with open('amazon_tmp.html', 'w') as amazon_tmp:
            amazon_tmp.write(data.text)

    def test_soup(self):
        with open('amazon_tmp.html', 'r') as amazon_data:
            soup = self.scraper.soup(amazon_data.read().strip()) 
            self.assertNotEqual(soup, None)
            self.assertEqual(
                    soup.title.string.split(':')[0].strip(), 'Amazon.in')

    def test_get_items(self):
        with open('amazon_tmp.html', 'r') as amazon_data:
            soup = self.scraper.soup(amazon_data.read().strip())
            items = self.scraper.get_items(soup)
            self.assertGreater(len(items), 0)
            for item in items:
                '''
                Not testing reviews and rating since some products don't 
                have reviews or ratings
                '''
                self.assertGreater(len(''.join(item.name)), 0)
                self.assertGreater(len(''.join(item.img)), 0)
                self.assertGreater(len(''.join(item.price)), 0)
                self.assertGreater(len(item.url), 0)


class TestFlipkartScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper.FlipkartScraper()
        self.query = choice(
                ['trading books', 'men sunglasses', 
                 'casio watches for men', 'the alchemist',
                 'iphone', 'samsung watches'])
        self.__fetch_data()

    def __fetch_data(self):
        data = self.scraper.fetch_data('vellathooval stephen')
        self.assertEqual(data.status_code, 200)
        with open('flipkart_tmp.html', 'w') as flipkart_tmp:
            flipkart_tmp.write(data.text)

    def test_soup(self):
        with open('flipkart_tmp.html', 'r') as flipkart_data:
            soup = self.scraper.soup(flipkart_data.read().strip()) 
            self.assertNotEqual(soup, None)
            self.assertEqual(
                    soup.title.string.split('|')[1].strip(), 'Flipkart.com')

    def test_get_items(self):
        with open('flipkart_tmp.html', 'r') as flipkart_data:
            soup = self.scraper.soup(flipkart_data.read().strip())
            items = self.scraper.get_items(soup)
            self.assertGreater(len(items), 0)
            for item in items:
                '''
                Not testing reviews and rating since some products don't 
                have reviews or ratings
                '''
                self.assertGreater(len(''.join(item.name)), 0)
                self.assertGreater(len(''.join(item.img)), 0)
                self.assertGreater(len(''.join(item.price)), 0)
                self.assertGreater(len(item.url), 0)

