# Создать страницу, на которой будет форма для ввода числа и кнопка "Отправить".
# При нажатии на кнопку будет произведено перенаправление на страницу с результатом,
# где будет выведено введенное число и его квадрат.

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

get_square = {'square': ''}


@app.route('/')
@app.route('/submit', methods=['POST', 'GET'])
def get():
    if request.method == 'POST':
        if name := request.form.get('name'):
            get_square['square'] = f'Квадрат числа {name}: {int(name) ** 2}'
            return redirect(url_for('square'))
        return redirect(url_for('get'))

    context = {'title': 'Квадрат числа',
               'name_button': 'Отправить',
               'type_date': 'number',
               'place_holder': 'Введите число'}
    return render_template('form.html', **context)


# @app.post('/submit/')
# def post():
#     name = request.form.get('name')
#     get_square['square'] = f'Квадрат числа {name} {int(name) ** 2:_}'
#     return redirect(url_for('square'))


@app.route('/square/')
def square():
    context = {'title': 'Квадрат числа', 'answer': get_square['square']}
    return render_template('answer.html', **context)


if __name__ == '__main__':
    app.run(debug=True)