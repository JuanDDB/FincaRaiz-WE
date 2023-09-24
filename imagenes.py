import os
import requests
from bs4 import BeautifulSoup
import shutil
import csv

csv_filename = 'C:\\Users\\Juan Dallos\\Desktop\\FincaRaiz-WE-main\\FincaRaiz-WE-main\\ofertas.csv'

enlaces = []

with open(csv_filename, 'r', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if 'enlace' in row:
            enlace = row['enlace']
            enlaces.append(enlace)

for index, enlace in enumerate(enlaces, start=671):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(enlace, headers=headers, allow_redirects=True)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_= 'jss234 jss236')
        
        if divs:
            carpeta_oferta = f'Oferta{index}'
            os.makedirs(carpeta_oferta, exist_ok=True)
            
            for i, div in enumerate(divs, start=1):
                img_tag = div.find('img')
                if img_tag:
                    img_url = img_tag['src']
                    print(f"URL de la imagen {i}: {img_url}")  
                    img_response = requests.get(img_url, stream=True)
                    if img_response.status_code == 200:
                        with open(os.path.join(carpeta_oferta, f'imagen_{i}.jpg'), 'wb') as img_file:
                            img_response.raw.decode_content = True
                            shutil.copyfileobj(img_response.raw, img_file)
                        print(f"Imagen {i} guardada en {carpeta_oferta}")
                    else:
                        print(f"No se pudo descargar la imagen {i}")
                else:
                    print(f"No se encontró la etiqueta img en el div")
        else:
            print(f"No se encontraron elementos con la clase 'jss224 jss226' en {enlace}")
    else:
        print(f"No se pudo acceder a {enlace}")

print("Proceso completado.")