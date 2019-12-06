import object_class, scraper, time  # importowanie potrzebnych bibliotek


# funkcja, która jest wywoływana przez formularz, jako dane wejściowe dostaje listę szukanych obiektów, a zwraca listę znalezionych obiektów
def StartScript(List_of_searched: object_class.ListOfSearched):
    #otwarcie i zapisywanie logów do pliku
    file = open("log.txt", "a")
    file.write("Czas rozpoczęcia wykonywania:" + time.ctime(time.time()) + "\n")
    file.close()
    #mierzenie czasu
    time_start = time.time()

    # -------------------wywołanie scrapera i zapisanie w zmiennej jako listy znalezionych obiektów klasy object_class.List
    Lof = scraplist(List_of_searched.ListOS)
    # logi i mierzenie czasu
    file = open("log.txt", "a")
    time_scrap = time.time()
    file.write("Czas całkowity scrapowania: " + str(round(time_scrap - time_start, 2)) + "s\n")
    # inicjalizacja zmiennej, do której będą wpisywane znalezione zestawy
    FoundSets = object_class.FoundSets()
    # sortowanie po cenie
    Lof.sort_list()
    #Logi
    time_sort = time.time()
    file.write("Czas sortowania: " + str(round(time_sort - time_start, 2)) + "s\n")
    # ---------------- Pętla wybierająca 3 najlepsze oferty z każdego produktu i wpisująca je do odpowiednich zestawów
    for i in Lof.lista:  # i to lista znalezionych ofert
        for k in range(0, 3):
            if len(i.lista) > 0:  # warunek zabezpieczający przed popowaniem pustej listy
                item = i.lista.pop(0)
                founditem = object_class.FoundItem(item.name, item.price * item.amount + item.price_ship, item.rate,
                                                   item.url, True)
            else:
                founditem = object_class.FoundItem('', 0, 0, '', False)
            FoundSets.add_to_list(k, founditem, founditem.price)
    # --------------------- Jeśli nie chcemy wyświetlać niepełnych zestawów należy odkomentować poniższy fragment
    # for lis in FoundSets.list:  # removal of unfilled lists
    #     for item in lis:
    #         if not item.is_found:
    #             FoundSets.list.remove(lis)

    # logi
    time_sets = time.time()
    file.write("Czas tworzenia zestawów i ich sprawdzania: " + str(round(time_sets - time_start, 2)) + "s\n")
    file.write("Czas całkowity wykonywania funkcji StartScript: " + str(round(time.time() - time_start, 2)) + "s\n")
    file.close()
    # zwracamy listę znalezionych zestawów
    return FoundSets


# funkcja wywołująca scraper i konwertująca dane uzyskane do obiektów klasy Object, Obj_list i List
def scraplist(list_of_searched):
    #mierzenie czasu i logi
    timeperscrap = []
    f = open("log.txt", "a")
    # powołanie zmiennej typu List
    foundlist = object_class.List(len(list_of_searched))
    # mierzenie czasu
    timeperscrap.append(time.time())

    #pętla wywołująca scraper i konwertująca dane dla każdego szukanego przedmiotu
    for item in list_of_searched:
        # scrapowanie
        scrap = scraper.Scraper(item.name)
        scrap.run()
        # tworzenie pustego obiektu
        foundobjlist = object_class.Obj_list()
        # konwersja ofert do obiektów
        for found in scrap.products_list:
            if not found["deliver_cost"] == None:
                foundobjlist.create_obj(found["name"], float(found["price"]), float(min(found["deliver_cost"])),
                                        int(found["rate"]),
                                        int(found["rate_number"]), int(item.amount), found["url"])
        #wpisanie do obiektu typu Lista obiektu Obj_list jako "podlisty"
        foundlist.set_objlist(list_of_searched.index(item), foundobjlist)
        # logi itp.
        timeperscrap.append(time.time())
    for timestamp in timeperscrap:
        if not timeperscrap.index(timestamp) == 0:
            f.write("czas wykonanie scrapu przedmiotu" + str(timeperscrap.index(timestamp)) + " wynosi: " + str(
                round(timestamp - timestart, 2)) + "s\n")
        timestart = timestamp
    f.close()
    # zwrócenie obiektu typu List
    return foundlist
