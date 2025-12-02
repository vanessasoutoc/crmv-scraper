from flask import Flask, jsonify, request
from flasgger import Swagger
from crmv_scraper import CRMVScraper

app = Flask(__name__)
swagger = Swagger(app)
scraper = CRMVScraper()

@app.route('/')
def hello():
    """
    Hello World endpoint
    ---
    responses:
      200:
        description: Welcome message
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Hello, World!"
    """
    return jsonify({"message": "Hello, World!"})

@app.route('/api/health')
def health():
    """
    Health check endpoint
    ---
    responses:
      200:
        description: API health status
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
    """
    return jsonify({"status": "healthy"})

@app.route('/api/crmv/<crmv_number>/<state>')
def find_crmv(crmv_number, state):
    """
    Search CRMV by number and state
    ---
    parameters:
      - name: crmv_number
        in: path
        type: string
        required: true
        description: CRMV registration number
        example: "02655"
      - name: state
        in: path
        type: string
        required: true
        description: State abbreviation
        example: "MG"
    responses:
      200:
        description: CRMV information found
        schema:
          type: object
          properties:
            type:
              type: string
              example: "success"
            data:
              type: array
              items:
                type: object
                properties:
                  nome:
                    type: string
                    example: "CLAUDIO BARRETO"
                  pf_inscricao:
                    type: string
                    example: "02655"
                  pf_uf:
                    type: string
                    example: "MG"
                  atuante:
                    type: boolean
                    example: true
      400:
        description: Error occurred
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Failed to get reCAPTCHA token"
    """
    result = scraper.search_crmv(crmv_number, state)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)