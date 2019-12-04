import object_class, scraper

def StartScript(List_of_searched:object_class.ListOfSearched):
    Lof = scraplist(List_of_searched.ListOS)
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
        if len(l) < len(List_of_searched.ListOS):
            FoundSets.list.remove(l)

    return FoundSets
    pass


def scraplist(list_of_searched):
    foundlist = object_class.List(len(list_of_searched))
    for item in list_of_searched:
        scrap = scraper.Scraper(item.name)
        scrap.run()
        foundobjlist = object_class.Obj_list()
        for found in scrap.products_list:
            if not found["deliver_cost"] == None:
                foundobjlist.create_obj(found["name"], found["price"], min(found["deliver_cost"]), found["rate"],
                                        found["rate_number"])
        foundlist.set_objlist(list_of_searched.index(item), foundobjlist)
    return foundlist
