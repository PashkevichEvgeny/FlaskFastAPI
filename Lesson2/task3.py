# Создать страницу, на которой будет форма для ввода логина и пароля.
# При нажатии на кнопку "Отправить" будет произведена проверка соответствия логина и пароля
# и переход на страницу приветствия пользователя или страницу с ошибкой.

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.get('/submit')
def get():
    context = {'title': 'Авторизация', 'name_button': 'Войти'}
    return render_template('loginpassword.html', **context)


@app.post('/submit/')
def post():
    name, password = request.form.get('name'), request.form.get('password')
    if not name or not password:
        return redirect(url_for('get'))
    res = f'Привет, {name}' if (name.lower(), password) == ('admin', 'qwerty') else 'Неверные данные.'
    context = {'title': 'Ответ сервера', 'answer': res}
    return render_template('answer.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
