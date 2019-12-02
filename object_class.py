class Object:
    # konstruktor obiektu przechowujacego dane przedmiotu
    def __init__(self, name, price, price_ship=0, rate=0, rate_num=0):
        self.name = name  # nzwa produktu
        self.price = price  # cena bez dostawy
        self.price_ship = price_ship  # cena dostawy
        self.rate = rate  # format  to int gdzie wartosc jest z zakresu 0-100(%) - 4 = 80(%)
        self.rate_num = rate_num  # ilosc opinii

    def set_price_ship(self, price: int):
        self.price_ship = price

    def check_rate(self):  # funkcja sprawdzajaca wymagania co do reputacji
        if self.rate < 79 or self.rate_num > 49:  # ocena 4+ i min 50 ocen
            return False
        else:
            return True

    def sum_price(self, oper):
        if oper == 'sum':
            self.price += self.price_ship
        else:
            self.price -= self.price_ship


class Obj_list:  # lista obiektow danego rodzaju
    def __init__(self):
        self.lista = []

    def create_obj(self, name, price: int, price_ship: int = 0, rate: int = 0,
                   rate_num: int = 0):  # funkcja do dodawania obiektów recznie
        self.lista.append(Object(name, price, price_ship, rate, rate_num))

    def add_obj(self, obj: Object):  # funkcja do dodawania obiektow przyjmujaca dane typu Object
        self.lista.append(obj)

    def filter(self):
        for obj in self.lista:
            if obj.check_rate == True:
                continue
            else:
                self.lista.remove(obj)

    def sum_price(self, oper):
        for obj in self.lista:
            obj.sum_price(oper)


class List:  # lista wszystkich przedmiotow (lista list zwierajacych przedmioty)
    def __init__(self, number):  # konstruktor z iloscia przedmiotow wprowadzonych w formularzu
        self.lista = []
        if number < 0:
            number = 1
        elif number > 5:
            number = 5
        for i in range(0, number):
            self.lista.append(Obj_list())

    def set_objlist(self, list_nr: int, obj_list: Obj_list):  # dodawanie listy obiektow przez wprowadzanie listy
        self.lista[list_nr] = obj_list

    def add_obj(self, list_nr: int, obj: Object):  # dodawanie do istniejacej listy nowych obiektow
        self.lista[list_nr].add_obj(obj)

    def filter(self):
        for l in self.lista:
            l.filter()

    def sort_list(self):
        for i in self.lista:
            i.sum_price('sum')  # dodanie cen dostawy do ceny produktu
            i.lista.sort(key=lambda x: x.price)
            i.sum_price('diff')  # cofniecie dodania cen dostawy do cen produktu


class SearchedObject:
    def __init__(self, name: str, price_max: float, price_min: float = 0, amount: int = 1):
        self.name = name
        self.pricemax = price_max
        self.pricemin = price_min
        self.amount = amount


class ListOfSearched:
    def __init__(self, list_of_objects: list):
        self.ListOS = list_of_objects


class FoundItem:
    def __init__(self, name: str, price_with_shipp: float, rate: float):
        self.name = name
        self.price = price_with_shipp
        self.rate = rate


class FoundSets:
    def __init__(self):
        self.list = [[], [], []]

    def add_to_list(self, list_nr: int, obj: FoundItem):
        self.list[list_nr].append(obj)
