from flask import Flask, render_template, jsonify
from scrapers.scraper import AmazonScraper


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.get('/fetch/<query>')
def fetch_data(query):
    amazon_scraper = AmazonScraper()
    data = amazon_scraper.fetch_data(query)
    soup = amazon_scraper.soup(data.text)
    data_dict = amazon_scraper.get_items(soup, limit=5)
    items = []
    for item in data_dict:
        items.append(item.get())
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
