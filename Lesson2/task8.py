# Создать страницу, на которой будет форма для ввода имени и кнопка "Отправить"
# При нажатии на кнопку будет произведено перенаправление на страницу с flash сообщением,
# где будет выведено "Привет, {имя}!".

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

get_name = {'name': ''}


@app.route('/')
@app.get('/submit')
def get():
    context = {'title': 'Отправить имя'}
    return render_template('flash.html', **context)


@app.post('/submit/')
def post():
    name = request.form.get('name')
    if not name:
        flash('Введите имя!', 'danger')
        return redirect(url_for('get'))
    flash(f'Привет, {name}!', 'success')
    return redirect(url_for('get'))


if __name__ == '__main__':
    app.run(debug=True)
