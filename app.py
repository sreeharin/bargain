from flask import Flask, render_template
from scraper.scraper import AmazonScraper, FlipkartScraper

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html'), 200


@app.get('/best-deals/<query>')
def best_deals(query):
    amazon_scraper = AmazonScraper()
    flipkart_scraper = FlipkartScraper()

    amazon_data = amazon_scraper.fetch_data(query)
    amazon_soup = amazon_scraper.soup(amazon_data.text)
    amazon_results = amazon_scraper.get_items(amazon_soup)

    flipkart_data = flipkart_scraper.fetch_data(query)
    flipkart_soup = flipkart_scraper.soup(flipkart_data.text)
    flipkart_results = flipkart_scraper.get_items(flipkart_soup)

    results = {'amazon': [], 'flipkart': []}

    for result in amazon_results:
        results['amazon'].append(result.get())

    for result in flipkart_results:
        results['flipkart'].append(result.get())

    return results, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
