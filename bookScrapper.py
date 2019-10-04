from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup


def getAndPaginateUrls():
    print("Se esta paginando el contenido del sitio, por favor espere...")

    pages = []
    next_page = "http://books.toscrape.com/catalogue/page-1.html"
    while requests.get(next_page).status_code == 200:
        pages.append(next_page)
        next_page = pages[-1].split("-")[0] + "-" + str(
            int(pages[-1].split("-")[1].split(".")[0]) + 1) + ".html"

    return pages


# metodo para obtener la url de cada libro de la siguiente
# forma http://books.toscrape.com/catalogue/'nombre-de-libro'/index.html
def getUrlBook(url):
    soup = getAndParseURL(url)
    return ['/'.join(url.split('/')[:-1]) + '/' +
            title.div.a.get('href') for title in soup.find_all('article', class_='product_pod')]


def scrappingBookData(books):

    titles = []
    prices = []
    number_stock = []
    categories = []
    img_covers = []
    reviews = []
    upcs = []
    types_products = []
    prices_excl_tax = []
    prices_incl_tax = []
    taxes = []
    availabilities = []
    num_reviews = []

    print("Recopilando datos de cada libro, esto llevara bastante tiempo, por favor espere...")

    for book in books:

        soup = getAndParseURL(book)

        titles.append(soup.find('div', class_=re.compile('product_main')).h1.text)
        prices.append(soup.find('p', class_='price_color').text[2:])
        number_stock.append(re.sub("[^0-9]", "", soup.find('p', class_='instock availability').text))
        categories.append(soup.find('a', href=re.compile('../category/books/')).get('href').split('/')[3])
        img_covers.append(book.replace('index.html', '') + soup.find('img').get('src'))
        reviews.append(soup.find('p', class_=re.compile('star-rating')).get('class')[1])

        table = soup.find('table', class_='table table-striped')
        table_data = []

        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                table_data.append(td.text)

        upcs.append(table_data[0])
        types_products.append(table_data[1])
        prices_excl_tax.append(re.sub("[^0-9.]", "", table_data[2]))
        prices_incl_tax.append(re.sub("[^0-9.]", "", table_data[3]))
        taxes.append(re.sub("[^0-9.]", "", table_data[4]))
        availabilities.append(table_data[5])
        num_reviews.append(table_data[6])

        scraped_data = pd.DataFrame({
                              'TITLE': titles,
                              'PRICE': prices,
                              'STOCK': number_stock,
                              'CATEGORY': categories,
                              'COVER': img_covers,
                              'UPC': upcs,
                              'PRODUCT TYPE': types_products,
                              'PRICE (EXCL TAX)': prices_excl_tax,
                              'PRICE (INCL TAX)': prices_incl_tax,
                              'TAX': taxes,
                              'AVAILABILITY': availabilities,
                              'N° OF REVIEWS': num_reviews
                              })

    return scraped_data


main_url = 'http://books.toscrape.com/'

print("Iniciando Web Scrapping de "+main_url)

pages = getAndPaginateUrls()

print("Se obtuvieron " + str(len(pages)) + " urls de paginacion para el sitio web")
print("Se muestran las 5 primeras url de la paginacion")
print(pages[:5])

print("Obteniendo los link de cada libro, por favor espere...")

books = []
for page in pages:
    books.extend(getUrlBook(page))

print(str(len(books)) + ' links de libros recolectados')
print("Se muestran las 5 primeros links de libros obtenidos: ")
print(books[:5])

scraped_data = scrappingBookData(books)

print("Mostrando las primeras 5 filas del archivo a generar")
print(scraped_data.head())

print("Generando archivo bookScrapping.csv ...")

scraped_data.to_csv('bookScrapping.csv', encoding='utf-8', index=False)

print("Archivo bookScrapping.csv generado correctamente.")

