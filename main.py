import argparse
import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_FOUNDED = 1920


def get_sorted_wines(wines):
    sorted_wines = collections.defaultdict(list)
    for wine in wines:
        sorted_wines[wine['Категория']].append(
            {
                'Название': wine['Название'],
                'Сорт': wine['Сорт'],
                'Цена': wine['Цена'],
                'Картинка': wine['Картинка'],
                'Акция': wine['Акция']
            }
        )
    return sorted_wines


def get_year_form(year):
    last_two_chars = str(year)[-2:]
    if int(last_two_chars) > 4 and int(last_two_chars) < 21:
        return 'лет'
    last_char = str(year)[-1:]
    if int(last_char) == 1:
        return 'год'
    if int(last_char) in (2, 3, 4):
        return 'года'
    return 'лет'


def main():
    winery_age = datetime.datetime.now().year - WINERY_FOUNDED
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='wine.xlsx', required=False)
    args = parser.parse_args()
    wines_table = pandas.read_excel(
            args.file, na_values=['Nan', 'nan'], keep_default_na=False
    )
    products = wines_table.to_dict(orient='records')
    sorted_products = get_sorted_wines(products)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        products=sorted_products,
        winery_age=winery_age,
        year_form=get_year_form(winery_age)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
