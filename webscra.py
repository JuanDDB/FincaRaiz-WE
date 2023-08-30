from selenium import webdriver
from selenium.webdriver.common.by import By

def obtener_enlaces_totales():
    # Configurar Selenium
    driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado y en tu PATH

    # Inicializar una lista para almacenar los enlaces
    enlaces_totales = []

    # Iterar a través de las 40 páginas
    for pagina in range(1, 2):
        # Construir la URL de la página actual
        url = f"https://www.fincaraiz.com.co/finca-raiz/venta/bogota/bogota-dc?usado=true&pagina={pagina}"
        
        # Abrir la página
        driver.get(url)
        
        # Encontrar todos los elementos div que contienen los enlaces
        divs = driver.find_elements(By.XPATH, '//*[@id="listingContainer"]/div/article/a')
        
        # Iterar a través de los elementos div y extraer los enlaces
        for div in divs:
            enlace = div.get_attribute("href")
            enlaces_totales.append(enlace)
        
    # Cerrar el navegador
    driver.quit()
    
    return enlaces_totales
