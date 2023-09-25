import os
import requests
from bs4 import BeautifulSoup
import shutil
import csv
import pandas as pd

csv_filename = 'C:\\Users\\Juan Dallos\\Desktop\\FincaRaiz-WE-main\\FincaRaiz-WE-main\\ofertas.csv'

enlaces = []

df = pd.read_csv(csv_filename, delimiter=',', encoding='utf-8')

enlaces_df = df['enlace']

print(enlaces_df)

for index, enlace in enumerate(enlaces_df, start=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(enlace, headers=headers, allow_redirects=True)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='jss234 jss236')

        if divs:
            carpeta_oferta = f'Oferta{index}'
            os.makedirs(carpeta_oferta, exist_ok=True)

            for i, div in enumerate(divs, start=1):
                img_tag = div.find('img')
                if img_tag:
                    img_url = img_tag['src']
                    print(f"URL de la imagen {i}: {img_url}")
                    try:
                        img_response = requests.get(img_url, stream=True)
                        img_response.raise_for_status()
                        with open(os.path.join(carpeta_oferta, f'imagen_{i}.jpg'), 'wb') as img_file:
                            img_response.raw.decode_content = True
                            shutil.copyfileobj(img_response.raw, img_file)
                        print(f"Imagen {i} guardada en {carpeta_oferta}")
                    except requests.exceptions.RequestException as img_error:
                        print(f"No se pudo descargar la imagen {i}: {img_error}")
                else:
                    print(f"No se encontró la etiqueta img en el div")
        else:
            print(f"No se encontraron elementos con la clase 'jss224 jss226' en {enlace}")
    except requests.exceptions.RequestException as request_error:
        print(f"No se pudo acceder a {enlace}: {request_error}")

print("Proceso completado.")
