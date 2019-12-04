from flask import Flask, render_template, request
from object_class import SearchedObject, ListOfSearched
import StartScript

app = Flask(__name__)
#products = [[{'name': 'telefon', 'price': '20', 'link': 'https://www.google.com'}, {'name': 'telefon1', 'price': '201', 'link': 'https://www.google.com'}, {'name': 'telefon', 'price': '20', 'link': 'https://www.google.com'}, {'name': 'telefon', 'price': '20', 'link': 'https://www.google.com'}, {'name': 'telefon', 'price': '20', 'link': 'https://www.google.com'}], [{'name': 'telefon2', 'price': '202', 'link': 'https://www.google.com'}, {'name': 'telefon3', 'price': '203', 'link': 'https://www.google.com'}]]

@app.route('/')
def display_form():
    return render_template('query.html')

@app.route('/results')
def get_results():
    query = request.args

    searched_products = []

    product1 = SearchedObject(query["product1"], query["price-max1"], query["price-min1"], 
        query["amount1"])
    searched_products.append(product1)
    if query["product2"] != "":
        product2 = SearchedObject(query["product2"], query["price-max2"], query["price-min2"], 
            query["amount2"])
        searched_products.append(product2)
    if query["product3"] != "":
        product3 = SearchedObject(query["product3"], query["price-max3"], query["price-min3"], 
            query["amount3"])
        searched_products.append(product3)
    if query["product4"] != "":
        product4 = SearchedObject(query["product4"], query["price-max4"], query["price-min4"], 
            query["amount4"])
        searched_products.append(product4)
    if query["product5"] != "":
        print("product5 is not NONE")
        product5 = SearchedObject(query["product5"], query["price-max5"], query["price-min5"], 
            query["amount5"])
        searched_products.append(product5)

    searched_objects = ListOfSearched(searched_products)

    FoundSets = StartScript.StartScript(searched_objects)

    return render_template('result.html', results = FoundSets.list, price_list = FoundSets.price)