import requests
from bs4 import BeautifulSoup
import json
import datetime

class Informador:
    def __init__(self):
        self.lista = []

    def to_json(self):
        with open(datetime.datetime.now().strftime('%Y-%m-%d')+ '.json', 'w')as archivo:
            json.dump(self.lista, archivo, sort_keys=False, indent=4)




    def scrapping(self,urla,tipe):
        url = urla
        r = requests.get(url)
        r.encoding = 'utf-8'
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        tipo=tipe
        # print(soup)
        items = soup.find_all(class_='items')

        # print(items)
        casas = items[0].find_all('li')
        if tipo == 1:
            self.scrapping_casas(casas)
        else:
            self.scrapping_rentas(casas)


        paginas = soup.find(class_="pagination")
        #
        # contain = soup.find(class_="dropdown")
        # print(contain)
        # tipe = contain.span.text
        #
        # print(tipe)

        paginas = paginas.find_all('li')
        urls = []

        i = 2
        while i < len(paginas) - 1:
            # print(paginas[i].a['href'])
            urls.append(paginas[i].a['href'])
            i = i + 1
        self.scrapping_paginas(urls,tipo)

    def scrapping_paginas(self, urls,tipo):
        for url in urls:

            r = requests.get(url)
            r.encoding = 'utf-8'
            # print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')

            # print(soup)
            items = soup.find_all(class_='items')
            # print(items)
            casas = items[0].find_all('li')
            if tipo==1:
                self.scrapping_casas(casas)
            else:
                self.scrapping_rentas(casas)




    def scrapping_casas(self, casas):
        for c in casas:
            casa = {
                "ubicacion": c.find_all(class_='location')[0].text,
                "titulo": c.a.text,
                "precio": c.h5.text,
                "descripcion": c.p.text,
                "recamaras": c.find(class_='info-rec').text,
                "m2": c.find(class_='info-m2').text,
                "m2_2": c.find(class_='info-m2-2').text,
                "wc": c.find(class_='info-wc').text,
                "cars": c.find(class_='info-cars').text,
                "colonia": c.find(class_='info-gps').contents[1],
                "imgs": ['http:' + i['src'] for i in c.find_all('img')],
                "tipo" : "venta"
            }
            self.lista.append(casa)


    def scrapping_rentas(self, casas):
        for c in casas:
            casa = {
                "ubicacion": c.find_all(class_='location')[0].text,
                "titulo": c.a.text,
                "precio": c.h5.text,
                "descripcion": c.p.text,
                "recamaras": c.find(class_='info-rec').text,
                "m2": c.find(class_='info-m2').text,
                "m2_2": c.find(class_='info-m2-2').text,
                "wc": c.find(class_='info-wc').text,
                "cars": c.find(class_='info-cars').text,
                "colonia": c.find(class_='info-gps').contents[1],
                "imgs": ['http:' + i['src'] for i in c.find_all('img')],
                "tipo" : "renta"
            }
            self.lista.append(casa)

