import csv
import concurrent.futures
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import namedtuple
from webscra import obtener_enlaces_totales

# Definición de la tupla "Oferta"
Oferta = namedtuple("Oferta", [
    "precio",
    "hab",
    "baños",
    "parqueaderos",
    "areaconstruida",
    "areaprivada",
    "estrato",
    "pison",
    "administración",
    "preciom",
    "coord",
])
lista_ofertas = []

enlaces = obtener_enlaces_totales()

def procesar_enlace(enlace):
    driver = webdriver.Chrome()
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
        
        precio_p = soup.select('p[class^="jss65 jss70"]')[1]
        precio = precio_p.get_text()
        coordenadas = driver.find_element('xpath', '//img[contains(@src, "snap_map")]')
        coord = coordenadas.get_attribute('src')

        if oferta_actual:
            lista_ofertas.append(Oferta(
                precio=precio,
                hab=oferta_actual.get('Habitaciones', ''),
                baños=oferta_actual.get('Baños', ''),
                parqueaderos=oferta_actual.get('Parqueaderos', ''),
                areaconstruida=oferta_actual.get('Área construída', ''),
                areaprivada=oferta_actual.get('Área privada', ''),
                estrato=oferta_actual.get('Estrato', ''),
                pison=oferta_actual.get('Piso N°', ''),
                administración=oferta_actual.get('Administración', ''),
                preciom=oferta_actual.get('Precio m²', ''),
                coord=coord
            ))
            oferta_actual = {}

    driver.quit()

# Procesar enlaces en paralelo
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(procesar_enlace, enlaces)

# Guardar los datos en un archivo CSV
csv_filename = "ofertas.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(Oferta._fields)  # Escribir la primera fila con los nombres de las columnas
    csv_writer.writerows(lista_ofertas)

print("Datos guardados en", csv_filename)
