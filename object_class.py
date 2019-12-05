class SearchedObject:
    def __init__(self, name: str, price_max: float, price_min: float = 0, amount: int = 1):
        self.name = name
        self.pricemax = price_max
        self.pricemin = price_min
        self.amount = amount


class Object:
    # konstruktor obiektu przechowujacego dane przedmiotu
    def __init__(self, name: str, price: float, price_ship: float = 0, rate: float = 0, rate_num: float = 0,
                 amount: int = 1, url: str = ''):
        self.name = name  # nzwa produktu
        self.price = price  # cena bez dostawy
        self.price_ship = price_ship  # cena dostawy
        self.rate = rate  # format  to int gdzie wartosc jest z zakresu 0-100(%) - 4 = 80(%)
        self.rate_num = rate_num  # ilosc opinii
        self.amount = amount
        self.url = url

    def set_price_ship(self, price: int):
        self.price_ship = price

    def check_req(self, ref_obj: SearchedObject):  # funkcja sprawdzajaca wymagania co do reputacji
        if self.rate > 79 and self.rate_num > 49 and self.price <= ref_obj.pricemax and self.price >= ref_obj.pricemin:  # ocena 4+ i min 50 ocen
            return False
        else:
            return True

    def sum_price(self, oper):
        if oper == 'sum':
            self.price = self.price * self.amount + self.price_ship
        else:
            self.price -= self.price_ship
            self.price = self.price / self.amount


class Obj_list:  # lista obiektow danego rodzaju
    def __init__(self):
        self.lista = []
        self.reference = None

    def set_reference(self, ref_obj: SearchedObject):
        self.reference = ref_obj

    def create_obj(self, name, price: float, price_ship: float = 0, rate: float = 0,
                   rate_num: int = 0, amount: int = 1, url: str = ''):  # funkcja do dodawania obiektów recznie
        self.lista.append(Object(name, price, price_ship, rate, rate_num, amount, url))

    def add_obj(self, obj: Object):  # funkcja do dodawania obiektow przyjmujaca dane typu Object
        self.lista.append(obj)

    def filter(self):
        for obj in self.lista:
            if obj.check_req(self.reference):
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

    def filter(self):  # for testing
        for l in self.lista:
            l.filter()


    def sort_list(self):
        for i in self.lista:
            i.sum_price('sum')  # dodanie cen dostawy do ceny produktu
            i.filter()
            i.lista.sort(key=lambda x: x.price)  # pytanie czy to ma tak być
            i.sum_price('rev')  # cofniecie dodania cen dostawy do cen produktu


class ListOfSearched:
    def __init__(self, list_of_objects: list):
        self.ListOS = list_of_objects


class FoundItem:
    def __init__(self, name: str, price_with_shipp: float, rate: float, url: str, is_found: bool):
        self.name = name
        self.price = price_with_shipp
        self.rate = rate
        self.url = url
        self.is_found = is_found


class FoundSets:
    def __init__(self):
        self.list = [[], [], []]
        self.price = [0, 0, 0]

    def add_to_list(self, list_nr: int, obj: FoundItem, price_change_summary: float):
        self.list[list_nr].append(obj)
        self.price[list_nr] += price_change_summary
