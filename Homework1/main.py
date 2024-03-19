# Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал),
# и дочерние шаблоны для страниц категорий товаров и отдельных товаров.
# Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.

from flask import Flask, render_template

app = Flask(__name__)


items = {'clothes': [
                 {'id': 1, 'name': 'Платье синее длинное', 'link': 1, 'price': 101},
                 {'id': 2, 'name': 'Костюм выпускной', 'link': 2, 'price': 102},
                 {'id': 3, 'name': 'Юбка', 'link': 3, 'price': 103}],
         'shoes': [
                 {'id': 4, 'name': 'Ботинок красный', 'link': 4, 'price': 202},
                 {'id': 5, 'name': 'Туфля черный', 'link': 5, 'price': 203},
                 {'id': 6, 'name': 'Сапоги для рыбалки', 'link': 6, 'price': 204}],
         'jackets': [
                 {'id': 7, 'name': 'Куртка теплая', 'link': 7, 'price': 305},
                 {'id': 8, 'name': 'Куртка летняя', 'link': 8, 'price': 306},
                 {'id': 9, 'name': 'Куртка зеленая', 'link': 9, 'price': 307}]}


@app.route('/')
@app.route('/catalog/')
def catalog():
    catalogs = [{'name': 'Одежда', 'link': 'catalog/clothes'},
                {'name': 'Обувь', 'link': 'catalog/shoes'},
                {'name': 'Куртка', 'link': 'catalog/jackets'},
                ]
    context = {'title': 'Каталог товаров', 'catalog': catalogs}
    return render_template('catalog.html', **context)


@app.route('/catalog/<subcategory>/')
def subcategory(subcategory):
    title = {'shoes': 'Обувь', 'clothes': 'Одежда', 'jackets': 'Куртка'}
    context = {'title': title[subcategory], 'items': items[subcategory]}
    return render_template('subcategory.html', **context)


@app.route('/<idd>/')
def item_page(idd):
    prod = {}
    for i in items.values():
        for j in i:
            if j['id'] == int(idd):
                prod = j
    context = {'p': prod}
    return render_template('item.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
