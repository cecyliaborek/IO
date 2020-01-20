# klasa do przechowywania informacji o szukanych obiektach
class SearchedObject:
    def __init__(self, name: str, price_max: float, price_min: float = 0, amount: int = 1):
        self.name = name
        self.pricemax = price_max
        self.pricemin = price_min
        self.amount = amount


# klasa do przechowywania informacji o znalezionych ofertach służąca do przetwarzania danych
class Object:
    # konstruktor
    def __init__(self, name: str, price: float, price_ship: float = 0, rate: float = 0, rate_num: float = 0,
                 amount: int = 1, url: str = ''):
        self.name = name  # nazwa produktu
        self.price = price  # cena bez dostawy
        self.price_ship = price_ship  # cena dostawy
        self.rate = rate  # format  to int gdzie wartosc jest z zakresu 0-100(%) - 4 = 80(%)
        self.rate_num = rate_num  # ilosc opinii
        self.amount = amount  # ilość sztuk
        self.url = url  # adres sklepu

    # metoda sprawdzająca czy dana oferta spełnia wymagania co do ceny i opinii - zwraca True jeśli spełnia
    def check_req(self, ref_obj: SearchedObject):  # metoda sprawdzajaca wymagania co do reputacji
        if self.rate > 79 and self.rate_num > 49 and self.price <= ref_obj.pricemax and self.price >= ref_obj.pricemin:  # ocena 4+ i min 50 ocen
            return False
        else:
            return True

    # metoda używana do podmiany ceny za sztukę na cene całościową(cena_za_szt*ilość_szt+cena_dostawy) i na odwrót w zależności od wywołania, używanie do sortowania
    def sum_price(self, oper):
        if oper == 'sum':
            self.price = self.price * self.amount + self.price_ship
        else:
            self.price -= self.price_ship
            self.price = self.price / self.amount


# klasa przechowująca listę obiektów typu Object i zawierająca operację filtracji
class Obj_list:
    # konstruktor
    def __init__(self):
        self.lista = []
        self.reference = None

    # dodanie przedmiotu o który pytał klient w celu sprawdzenia czy znaleziona oferta pasuje do wymagań zadanych np. cena max
    def set_reference(self, ref_obj: SearchedObject):
        self.reference = ref_obj

    # metoda tworząca nowy obiekt na końcu listy
    def create_obj(self, name, price: float, price_ship: float = 0, rate: float = 0,
                   rate_num: int = 0, amount: int = 1, url: str = ''):  # metoda do dodawania obiektów recznie
        self.lista.append(Object(name, price, price_ship, rate, rate_num, amount, url))

    # metoda doająca obiekt do końca listy
    def add_obj(self, obj: Object):  # metoda do dodawania obiektow przyjmujaca dane typu Object
        self.lista.append(obj)

    # fukncja filtrująca oferty i odrzucająca niepasujące do szukanych kryteriów
    def filter(self):
        for obj in self.lista:
            if obj.check_req(self.reference):
                continue
            else:
                self.lista.remove(obj)

    # metoda wywołująca metodę sum_price dla każdego obiektu w liście
    def sum_price(self, oper):
        for obj in self.lista:
            obj.sum_price(oper)


# klasa przechowująca listę list z ofertami (po 1 dla każdego szukanego przedmiotu)
class List:
    #konstruktor
    def __init__(self, number):  # konstruktor z iloscia przedmiotow wprowadzonych w formularzu
        self.lista = []
        if number < 0:
            number = 1
        elif number > 5:
            number = 5
        for i in range(0, number):
            self.lista.append(Obj_list())

    #metoda ustawiająca listę o dnym numerze na tą przekazaną w funkcji
    def set_objlist(self, list_nr: int, obj_list: Obj_list):  # dodawanie listy obiektow przez wprowadzanie listy
        self.lista[list_nr] = obj_list

    # metoda do dodawania ofert do danej listy ofert
    def add_obj(self, list_nr: int, obj: Object):  # dodawanie do istniejacej listy nowych obiektow
        self.lista[list_nr].add_obj(obj)

    # metoda do filtrowania i sortowania wg ceny znalezionych ofert
    def sort_list(self):
        for i in self.lista:
            i.sum_price('sum')  # dodanie cen dostawy do ceny produktu
            i.filter()
            i.lista.sort(key=lambda x: x.price)  # pytanie czy to ma tak być
            i.sum_price('rev')  # cofniecie dodania cen dostawy do cen produktu


# klasa do przechowywania listy szukanych przedmiotów (zwykła lista)
class ListOfSearched:
    def __init__(self, list_of_objects: list):
        self.ListOS = list_of_objects


# klasa do przechowywania informacji o znalezionych przedmiotach
class FoundItem:
    def __init__(self, name: str, price_with_shipp: float, rate: float, url: str, is_found: bool):
        self.name = name  # nazwa
        self.price = price_with_shipp  # cena z dostawą
        self.rate = rate  # ocena
        self.url = url  # link url
        self.is_found = is_found  # jeśli znaleziono ofertę, to zmienna ustawiona na True


# klasa do przechowywania zestawów (listy) znalezionych obiektów i infrmacji o ich sumarycznej cenie
class FoundSets:
    def __init__(self):
        self.list = [[], [], []]
        self.price = [0, 0, 0]  # cena sumaryczna zestawu, indeks odpowiada indeksowi przypisanego zestawu

    # metoda dodająca do zestawu znalezioną ofertę
    def add_to_list(self, list_nr: int, obj: FoundItem, price_change_summary: float):
        self.list[list_nr].append(obj)
        self.price[list_nr] += price_change_summary
