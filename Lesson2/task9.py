# Создать страницу, на которой будет форма для ввода имени и электронной почты.
# При отправке которой будет создан cookie файл с данными пользователя.
# Также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка "Выйти".
# При нажатии на кнопку будет удален cookie файл с данными пользователя
# и произведено перенаправление на страницу ввода имени и электронной почты.

from flask import Flask, render_template, request, redirect, url_for, make_response, Response

app = Flask(__name__)

get_name = {'name': ''}

answer = []


@app.route('/')
@app.get('/submit')
def get():
    context = {'title': 'Вход', 'name_button': 'Войти'}
    return render_template('loginmail.html', **context)


@app.post('/submit/')
def post():
    name, mail = request.form.get('name'), request.form.get('mail')
    if not name or not mail:
        return redirect(url_for('get'))
    response = make_response(render_template('greetings.html', **{'title': 'Приветствие', 'name': name}))
    answer.append(response)
    response.set_cookie('name', name)
    response.set_cookie('mail', mail)
    return redirect(url_for('greet'))


@app.route('/greetings/')
def greet():
    if len(answer):
        return answer[0]
    return redirect(url_for('get'))


@app.route('/logout/')
def logout():
    if not request.cookies.get('name'):
        return redirect(url_for('get'))
    response = make_response(render_template('logout.html', **{'title': 'Выход'}))
    response.delete_cookie('name')
    response.delete_cookie('mail')
    return response


if __name__ == '__main__':
    app.run(debug=True)
