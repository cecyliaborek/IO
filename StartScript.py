import object_class
import scraper, time


def StartScript(List_of_searched: object_class.ListOfSearched):
    file = open("log.txt", "a")
    file.write("Czas rozpoczęcia wykonywania:" + time.ctime(time.time()))
    time_start = time.time()
    Lof = scraplist(List_of_searched.ListOS)
    time_scrap = time.time()
    file.write("Czas całkowity scrapowania: " + str(round(time_scrap - time_start, 2)) + "s")
    FoundSets = object_class.FoundSets()
    Lof.sort_list()
    time_sort = time.time()
    file.write("Czas sortowania: " + str(round(time_sort - time_start, 2)) + "s")
    for i in Lof.lista:
        if len(i.lista) < 3:
            limit = len(i.lista)
        else:
            limit = 3

        for k in range(0, limit):
            if len(i.lista) > 0:
                item = i.lista.pop(0)
                founditem = object_class.FoundItem(item.name, item.price * item.amount + item.price_ship, item.rate,
                                                   item.url, True)
            else:
                founditem = object_class.FoundItem('', 0, 0, '', False)
            FoundSets.add_to_list(k, founditem, founditem.price)

    for lis in FoundSets.list:  # removal of unfilled lists
        for item in lis:
            if not item.is_found:
                FoundSets.list.remove(lis)
    time_sets = time.time()
    file.write("Czas tworzenia zestawów i ich sprawdzania: " + str(round(time_sets - time_start, 2)) + "s")
    file.write("Czas całkowity wykonywania funkcji StartScript: " + str(round(time.time() - time_start, 2)) + "s")
    return FoundSets


def scraplist(list_of_searched):
    timeperscrap = []
    f = open("log.txt", "a")
    foundlist = object_class.List(len(list_of_searched))
    for item in list_of_searched:
        timeperscrap.append(time.time())
        scrap = scraper.Scraper(item.name)
        scrap.run()
        foundobjlist = object_class.Obj_list()
        for found in scrap.products_list:
            if not found["deliver_cost"] == None:
                foundobjlist.create_obj(found["name"], float(found["price"]), float(min(found["deliver_cost"])),
                                        int(found["rate"]),
                                        int(found["rate_number"]), int(item.amount), found["url"])
        foundlist.set_objlist(list_of_searched.index(item), foundobjlist)
    timeperscrap.append(time.time())
    for timestamp in timeperscrap:
        if not timeperscrap.index(timestamp) == 0:
            f.write("czas wykonanie scrapu przedmiotu" + str(timeperscrap.index(timestamp)) + " wynosi: " + str(
                round(timestart - timestamp, 2)) + "s")
        timestart = timestamp

    return foundlist
