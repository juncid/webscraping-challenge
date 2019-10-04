from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


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

# creacion de listas para guardar los datos recolectados
titulos = []
precios = []
stocks = []
categorias = []
img_covers = []
reviews = []
upcs = []
tipos_de_producto = []
precios_sin_imp = []
precios_con_imp = []
imps = []
disponibilidades = []
num_reviews = []

print("Recopilando datos de cada libro, por favor sea paciente...")
# se itera la url de cada libro y se recaban los siguientes datos en un arreglo distinto:
#   titulo,precio,stock,categoria,imagen de portada,review,upc, tipo de producto, precio sin impuestos,
#   precio con impuestos, impuesto, disponibilidad, numero de reviews

for url in urls_libros:

    soup = obtener_y_codificar_url(url)

    titulos.append(soup.find('div', class_=re.compile('product_main')).h1.text)
    precios.append(soup.find('p', class_='price_color').text[2:])
    stocks.append(re.sub("[^0-9]", "", soup.find('p', class_='instock availability').text))
    categorias.append(soup.find('a', href=re.compile('../category/books/')).get('href').split('/')[3])
    img_covers.append(url.replace('index.html', '') + soup.find('img').get('src'))
    reviews.append(soup.find('p', class_=re.compile('star-rating')).get('class')[1])


    # Obtener datos de tabla, se itera dentro de esta para obtener todos
    # los valores dentro de los tag 'td' y ser añadidos a las listas
    # correspondientes.
    table = soup.find('table', class_='table table-striped')
    datos_tabla = []

    for tr in table.find_all('tr'):
        for td in tr.find_all('td'):
            datos_tabla.append(td.text)

    upcs.append(datos_tabla[0])
    tipos_de_producto.append(datos_tabla[1])
    precios_sin_imp.append(re.sub("[^0-9.]", "", datos_tabla[2]))
    precios_con_imp.append(re.sub("[^0-9.]", "", datos_tabla[3]))
    imps.append(re.sub("[^0-9.]", "", datos_tabla[4]))
    disponibilidades.append(datos_tabla[5])
    num_reviews.append(datos_tabla[6])

    # Creacion de un DataFrame el cual servira para la creacion del fichero
    # bookScrapping.csv
    datos_finales = pd.DataFrame({
                        'TITLE': titulos,
                        'PRICE': precios,
                        'STOCK': stocks,
                        'CATEGORY': categorias,
                        'COVER': img_covers,
                        'UPC': upcs,
                        'PRODUCT TYPE': tipos_de_producto,
                        'PRICE (EXCL TAX)': precios_sin_imp,
                        'PRICE (INCL TAX)': precios_con_imp,
                        'TAX': imps,
                        'AVAILABILITY': disponibilidades,
                        'N° OF REVIEWS': num_reviews
                        })

print("Mostrando las primeras 5 filas del archivo a generar")
print(datos_finales.head())

print("Generando archivo bookScrapping.csv ...")

datos_finales.to_csv('bookScrapping.csv', encoding='utf-8', index=False)

print("Archivo bookScrapping.csv generado correctamente.")
