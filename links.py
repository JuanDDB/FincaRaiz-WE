from selenium import webdriver
from selenium.webdriver.common.by import By

def obtener_enlaces_totales():
    driver = webdriver.Chrome()  

    enlaces_totales = []

    for pagina in range(1, 2):
        url = f"https://www.fincaraiz.com.co/apartamentos/venta/castilla/zona-occidental/bogota?usado=true&pagina={pagina}"
        driver.get(url)        
        divs = driver.find_elements(By.XPATH, '//*[@id="listingContainer"]/div/article/a')
        for div in divs:
            enlace = div.get_attribute("href")
            enlaces_totales.append(enlace)
        
    driver.quit()
    
    return enlaces_totales
