# Создать страницу, на которой будет кнопка "Нажми меня",
# при нажатии на которую будет переход на другую страницу с приветствием пользователя по имени.

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.get('/submit')
def get():
    context = {'title': 'Отправка имени',
               'name_button': 'Нажми МЕНЯ',
               'type_date': 'text',
               'place_holder': 'Введите имя'}
    return render_template('form.html', **context)


@app.post('/submit/')
def post():
    name = request.form.get('name')
    if not name:
        return redirect(url_for('get'))
    context = {'title': 'Приветствие', 'answer': f'Привет, {name}'}
    return render_template('answer.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
