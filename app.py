from flask import Flask, render_template, request
from object_class import SearchedObject, ListOfSearched
import StartScript
from object_class import FoundSets, FoundItem

app = Flask(__name__)


@app.route('/')
def display_form():
    return render_template('Query.html')


# def mock_result():
#     foundSets = FoundSets()
#     foundSets.add_to_list(0, FoundItem("Test1", 10.01, 2.03, "urrrllll", True), 1)
#     foundSets.add_to_list(0, FoundItem("Test1", 10.01, 2.03, "urrrllll", True), 1)
#     foundSets.add_to_list(0, FoundItem("Test1", 10.01, 2.03, "urrrllll", True), 1)
#     foundSets.add_to_list(0, FoundItem("Test1", 10.01, 2.03, "urrrllll", True), 1)
#     foundSets.add_to_list(0, FoundItem("Test1", 10.01, 2.03, "urrrllll", True), 1)
#     foundSets.add_to_list(1, FoundItem("Test2", 101.01, 22.03, "urrrllfdsdfsll", False), 2)
#     foundSets.add_to_list(1, FoundItem("Test2", 101.01, 22.03, "urrrllfdsdfsll", True), 2)
#     foundSets.add_to_list(1, FoundItem("Test2", 101.01, 22.03, "urrrllfdsdfsll", True), 2)
#     foundSets.add_to_list(1, FoundItem("Test2", 101.01, 22.03, "urrrllfdsdfsll", True), 2)
#     foundSets.add_to_list(1, FoundItem("Test2", 101.01, 22.03, "urrrllfdsdfsll", True), 2)
#     foundSets.add_to_list(2, FoundItem("Test3", 1220.01, 21.03, "fdsfsurrrllll", True), 5)
#     foundSets.add_to_list(2, FoundItem("Test3", 1220.01, 21.03, "fdsfsurrrllll", True), 5)
#     foundSets.add_to_list(2, FoundItem("Test3", 1220.01, 21.03, "fdsfsurrrllll", True), 5)
#     foundSets.add_to_list(2, FoundItem("Test3", 1220.01, 21.03, "fdsfsurrrllll", True), 5)
#     foundSets.add_to_list(2, FoundItem("Test3", 1220.01, 21.03, "fdsfsurrrllll", True), 5)
#     return foundSets

@app.route('/results')
def get_results():
    query = request.args

    searched_products = []

    product1 = SearchedObject(query["product1"], float(query["price-max1"]), float(query["price-min1"]),
                              int(query["amount1"]))
    searched_products.append(product1)
    if query["product2"] != "":
        product2 = SearchedObject(query["product2"], float(query["price-max2"]), float(query["price-min2"]),
                                  int(query["amount2"]))
        searched_products.append(product2)
    if query["product3"] != "":
        product3 = SearchedObject(query["product3"], float(query["price-max3"]), float(query["price-min3"]),
                                  int(query["amount3"]))
        searched_products.append(product3)
    if query["product4"] != "":
        product4 = SearchedObject(query["product4"], float(query["price-max4"]), float(query["price-min4"]),
                                  int(query["amount4"]))
        searched_products.append(product4)
    if query["product5"] != "":
        product5 = SearchedObject(query["product5"], float(query["price-max5"]), float(query["price-min5"]),
                                  int(query["amount5"]))
        searched_products.append(product5)

    searched_objects = ListOfSearched(searched_products)

    foundSets = StartScript.StartScript(searched_objects)
    
    return render_template('Result.html', results=foundSets.list, price_list=foundSets.price)
