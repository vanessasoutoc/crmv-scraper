from flask import Flask, jsonify, request
from crmv_scraper import CRMVScraper

app = Flask(__name__)
scraper = CRMVScraper()

@app.route('/')
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/crmv/<crmv_number>/<state>')
def find_crmv(crmv_number, state):
    result = scraper.search_crmv(crmv_number, state)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)