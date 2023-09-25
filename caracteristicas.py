import csv
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from collections import namedtuple
from links import obtener_enlaces_totales

Oferta = namedtuple("Oferta", [
    "carac",
    "precio",
    "hab",
    "baños",
    "parqueaderos",
    "areaconstruida",
    "areaprivada",
    "estrato",
    "pison",
    "administración",
    "coord",
    "enlace",  
])

lista_ofertas = []


enlaces = obtener_enlaces_totales()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")

def procesar_enlace(enlace):
    try:
        
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(enlace)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")

            divs_con_clase = soup.find_all("div", class_="MuiBox-root jss331 jss329")

            nombre_elemento = None
            oferta_actual = {}

            for div in divs_con_clase:
                elementos_p = div.select('p[class^="jss65 jss74"]')

                for p in elementos_p:
                    if nombre_elemento is None:
                        nombre_elemento = p.get_text()
                    else:
                        valor_elemento = p.get_text()
                        oferta_actual[nombre_elemento] = valor_elemento
                        nombre_elemento = None

            precio_p = soup.select('p[class^="jss65 jss70"]')
            if precio_p:
                precio = precio_p[1].get_text()
            else:
                precio = ""

            coordenadas = driver.find_element("css selector", 'img[src*="snap_map"]')
            coord = coordenadas.get_attribute('src')

            elementos_p = soup.find_all("p")
            hab = None  
            for p in elementos_p:
                if p.get_text() == "Habitaciones":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        hab = siguiente_p.get_text()
                        break  
            baños = None  
            for p in elementos_p:
                if p.get_text() == "Baños":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        baños = siguiente_p.get_text()
                        break  
            parqueaderos = None  
            for p in elementos_p:
                if p.get_text() == "Parqueaderos":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        parqueaderos = siguiente_p.get_text()
                        break  
            areaconstruida = None  
            for p in elementos_p:
                if p.get_text() == "Área construída":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        areaconstruida = siguiente_p.get_text()
                        break  
            areaprivada = None  
            for p in elementos_p:
                if p.get_text() == "Área privada":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        areaprivada = siguiente_p.get_text()
                        break  
            estrato = None  
            for p in elementos_p:
                if p.get_text() == "Estrato":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        estrato = siguiente_p.get_text()
                        break  
            pison = None  
            for p in elementos_p:
                if p.get_text() == "Piso N°":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        pison = siguiente_p.get_text()
                        break  
            administración = None  
            for p in elementos_p:
                if p.get_text() == "Administración":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        administración = siguiente_p.get_text()
                        break     
            carac = None  
            for p in elementos_p:
                if p.get_text() == "Descripción general":
                    siguiente_p = p.find_next("p")  
                    if siguiente_p:
                        carac = siguiente_p.get_text()
                        break    
                 
            precio_p = soup.select('p[class^="jss65 jss70"]')
            if precio_p:
                precio = precio_p[1].get_text()
            else:
                precio = ""

            coordenadas = driver.find_element("css selector", 'img[src*="snap_map"]')
            coord = coordenadas.get_attribute('src')
            lista_ofertas.append(Oferta(
                carac=carac,
                precio=precio,
                hab=hab,
                baños=baños,
                parqueaderos=parqueaderos,
                areaconstruida=areaconstruida,
                areaprivada=areaprivada,
                estrato=estrato,
                pison=pison,
                administración=administración,
                coord=coord,
                enlace=enlace 
            ))
            oferta_actual = {}

    except Exception as e:
        print(f"Error en el enlace {enlace}: {str(e)}")

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(procesar_enlace, enlace) for enlace in enlaces]

csv_filename = "ofertas.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(Oferta._fields)  
    csv_writer.writerows(lista_ofertas)

print(f"Datos guardados en {csv_filename}")
