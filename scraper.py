from bs4 import BeautifulSoup
import requests
import re


class Scraper:
    """
    Tworzac obiekt Scraper musimy podac jako argument stringa z nazwa szukanego produtu
    Metoda run() wlacza Scraper
    Atrybut products_list po wykonaniu wyszukiwania jest lista znalezionych produktow wraz z informacjami o nich
    Struktura:
    lista slownikow w srodku
    [ product1_dictionary, product2_dictionary, ... productX_dictionary]
    gdzie product1_dictionary ... productX_dictionary to
    {'name': qqq, 'price': www, 'rate':eee, 'rate_number': rrr, 'url': ttt, 'deliver_cost': yyy}

    qqq -> <class 'str'>    nazwa produktu w serwisie
    www -> <class 'float'>  cena produktu w serwisie
    eee -> <class 'float'>  ocena sklepu w serwisie
    rrr -> <class 'int'>    ilosc ocen sklepu w serwisie
    ttt -> <class 'str'>    link do sklepu w serwisie
    yyy -> <class 'list'>   lista zawierajaca ceny wysylki -> [<class 'float'>, <class 'float'>, ... ]
                            jezeli lista zawiera jeden element i jest to 0 to znaczy, ze wysylka za darmo!

                            UWAGA! Jezeli zamiast listy jest !!!None!!! to znaczy, ze strona z kosztami wysylki
                            nie dziala, lub jest to strona zewnetrzna, nie nalezaca do serwisu
    """
    def __init__(self, product_name):
        self.url = "https://www.skapiec.pl/szukaj/w_calym_serwisie/" \
                   + product_name.replace(' ', '+')                         # link do wyszukania produktu na stronie
        self.link = []
        self.products_list = []                                             # lista wyszukanych produktow
        self.source = None                                                  # pobrany dokument html

    def run(self):
        self.get_links()
        self.scrap()

    def get_links(self):
        self.get_html(self.url)
        soup = BeautifulSoup(self.source, 'lxml')
        for links in soup.find_all('a', attrs="hfref", class_='compare-link-1'):
            self.link.append('https://www.skapiec.pl' + links.get('href'))
            break
        if len(self.link) == 0:
            self.link.append(self.url)


    def get_html(self, url):
        self.source = requests.get(url).text

    def scrap(self):
        for links in self.link:
            self.get_html(links)
            soup = BeautifulSoup(self.source, 'lxml')
            for offer in soup.find_all('a', class_="offer-row-item"):
                product_list = {}
                self.scrap_product_name(offer, product_list)
                self.scrap_product_price(offer, product_list)
                self.scrap_product_rate(offer, product_list)
                self.scrap_product_rate_number(offer, product_list)
                self.scrap_product_shop_link(offer, product_list)
                self.scrap_if_delivery_cost(offer, product_list)
                self.products_list.append(product_list)

    def scrap_product_name(self, offer, product_list):
        name = offer.find('span', class_='description gtm_or_name')
        product_list['name'] = " ".join((name.text.replace('\n', '')).split())

    def scrap_product_price(self, offer, product_list):
        price = offer.find('span', class_='price gtm_or_price')
        product_list['price'] = float(price.text.replace(' ', '').replace('zł', '').replace(',', '.'))

    def scrap_product_rate(self, offer, product_list):
        rate = offer.find('div', attrs='data-decription', class_='shop-rating gtm_stars')
        if rate is not None:
            product_list['rate'] = (eval(rate.get('data-description')))['avg']
        else:
            product_list['rate'] = 0

    def scrap_product_rate_number(self, offer, product_list):
        rate_number = offer.find('span', attrs='data-label', class_='counter')
        if rate_number is not None:
            product_list ['rate_number'] = int(rate_number.text)
        else:
            product_list['rate_number'] = 0

    def scrap_product_shop_link(self, offer, product_list):
        product_list['url'] = 'https://www.skapiec.pl' + offer.get('href')

    def scrap_if_delivery_cost(self, offer, product_list):
        if_delivery_cost = offer.find(class_='delivery-cost')
        if if_delivery_cost.get('href') is None:
            product_list['deliver_cost'] = [0]
        else:
            self.scrap_delivery_cost(if_delivery_cost, product_list)

    def scrap_delivery_cost(self, offer, product_list):
        if offer.get('href').startswith('/delivery'):
            url = 'https://www.skapiec.pl' + offer.get('href')
            self.get_html(url)
            soup_delivery = BeautifulSoup(self.source, 'lxml')
            costs = self.scrap_html_table(soup_delivery)
            if len(costs) != 0:
                product_list['deliver_cost'] = costs
            else:
                product_list['deliver_cost'] = None
        else:
            product_list['deliver_cost'] = None

    def scrap_html_table(self, soup):
        product_delivery_cost = []
        for elements in soup.find_all(class_='even'):
            key = elements.text.replace('\n', '')
            product_delivery_cost.append(float((re.findall("\d+\.\d+ zł"," ".join(key.split())))[0].replace(' zł', '')))
        for elements in soup.find_all(class_='odd'):
            key = elements.text.replace('\n', '')
            product_delivery_cost.append(float((re.findall("\d+\.\d+ zł"," ".join(key.split())))[0].replace(' zł', '')))
        return product_delivery_cost


if __name__ == "__main__":
    scrap = Scraper('Cyberpunk 2077')
    scrap.run()
    for el in scrap.products_list:
        print(el)
    print(len(scrap.products_list))
