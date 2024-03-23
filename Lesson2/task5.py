# Создать страницу, на которой будет форма для ввода двух чисел и выбор операции
# (сложение, вычитание, умножение, деление) и кнопка "Вычислить".
# При нажатии на кнопку будет произведено вычисление результата выбранной операции и переход на страницу с результатом.
from math import inf

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

calc_result = {'result': ''}


def calc(a, b, operation):
    if operation == '+':
        return a + b
    if operation == '-':
        return a - b
    if operation == '*':
        return a * b
    if operation == '/' and b == 0:
        return inf
    if operation == '/':
        return a / b


@app.route('/')
@app.get('/submit')
def get():
    context = {'title': 'Калькулятор', 'name_button': 'Результат'}
    return render_template('calcform.html', **context)


@app.post('/submit/')
def post():
    a, b = request.form.get('a'), request.form.get('b')
    if not all(map(str.isdigit, (a, b))):
        return redirect(url_for('get'))
    else:
        a, b = map(int, (a, b))
    operation = request.form.get('operation')[-1]
    calc_result['result'] = f'Ответ: {a} {operation} {b} = {calc(a, b, operation)}'
    return redirect(url_for('calc_page'))


@app.route('/calculator/')
def calc_page():
    context = {'title': 'Результат вычислений', 'answer': calc_result['result']}
    return render_template('answer.html', **context)


if __name__ == '__main__':
    app.run(debug=True)