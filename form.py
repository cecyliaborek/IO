from flask import Flask, render_template, request

app = Flask(__name__)
products = [[{'name': 'telefon', 'price': '20', 'link': 'https://www.google.com'}, {'name': 'telefon1', 'price': '201', 'link': 'https://www.google.com'}, {'name': 'telefon', 'price': '20', 'link': 'https://www.google.com'}, {'name': 'telefon', 'price': '20', 'link': 'https://www.google.com'}, {'name': 'telefon', 'price': '20', 'link': 'https://www.google.com'}], [{'name': 'telefon2', 'price': '202', 'link': 'https://www.google.com'}, {'name': 'telefon3', 'price': '203', 'link': 'https://www.google.com'}]]

@app.route('/')
def display_form():
    return render_template('query.html')

@app.route('/results')
def get_results():
    query = request.args
    print(query)
    return render_template('result.html', results = products)