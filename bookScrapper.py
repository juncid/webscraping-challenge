from bs4 import BeautifulSoup
import requests


# metodo para obtener los datos de una url y convertir
# esta en codigo html legible
def obtener_y_codificar_url(url):
    resultado = requests.get(url)
    soup = BeautifulSoup(resultado.text, 'html.parser')
    return soup

# Metodo para obtener la paginacion del sitio el cual sera
# guardado en una lista llamada url_paginas
def obtener_urls_paginas():
    print("Se esta paginando el contenido del sitio, por favor espere...")
    url_paginas=[]

    # Se obtiene el total de paginacion del sitio, se evalua cada posible paginacion
    # si esta no entrega un status_code igual a 200, se reconocera como una pagina
    # inexistente y se terminara la paginacion.

    pagina_siguiente = "http://books.toscrape.com/catalogue/page-1.html"
    while requests.get(pagina_siguiente).status_code == 200:
        url_paginas.append(pagina_siguiente)
        pagina_siguiente = url_paginas[-1].split("-")[0] + "-" + str(
            int(url_paginas[-1].split("-")[1].split(".")[0]) + 1) + ".html"

    return url_paginas


main_url = 'http://books.toscrape.com/'

print("Iniciando Scrapping de "+main_url)


url_paginas = obtener_urls_paginas()

print("Se obtuvieron "+str(len(url_paginas))+" urls de paginacion para el sitio web")
print("Se muestran las 5 primeras url de la paginacion")
print(url_paginas[:5])

print("Obteniendo los link de cada libro, por favor espere...")
urls_libros = []

for pagina in url_paginas:
    urls_libros.extend(obtener_url_libro(pagina))

print(str(len(urls_libros)) + ' links de libros recolectados')
print("Se muestran las 5 primeros links de libros obtenidos: ")
print(urls_libros[:5])