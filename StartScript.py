import object_class

def StartScript(List_of_searched:object_class.ListOfSearched):
    #tu funkcja od michała prawdopodobie
    #Lof = funkcja_michała() # List of found - acronym
    #Lof.sort_list()
    Lof = object_class.List()
    FoundSets = object_class.FoundSets()
    for i in Lof.lista:
        if len(i) < 3:
            limit = len(i)
        else:
            limit = 3

        for k in range(0, limit):
            item = i.pop(0)
            founditem = object_class.FoundItem(item.name, item.price * item.amount + item.price_ship, item.rate)
            FoundSets.add_to_list(k, founditem, founditem.price)

    for l in FoundSets.list:  # removal of unfilled lists
        if len(l) < 5:
            FoundSets.list.remove(l)

    return FoundSets
    pass