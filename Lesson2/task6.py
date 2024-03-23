# Создать страницу, на которой будет форма для ввода имени и возраста пользователя и кнопка "Отправить".
# При нажатии на кнопку будет произведена проверка возраста и переход на страницу с результатом
# или на страницу с ошибкой в случае некорректного возраста.

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

get_age = {'age': 0}


@app.route('/')
@app.get('/submit')
def get():
    context = {'title': 'Проверка возраста', 'name_button': 'Отправить'}
    return render_template('ageform.html', **context)


@app.post('/submit/')
def post():
    name, age = request.form.get('name'), request.form.get('age')
    if not name or not age:
        return redirect(url_for('get'))
    get_age['age'] = int(age)
    return redirect(url_for('age_page'))


@app.route('/age-ok/')
def age_page():
    if get_age['age'] >= 18:
        context = {'title': 'Проверка пройдена', 'answer': f"Возраст {get_age['age']}, вход разрешен."}
        return render_template('answer.html', **context)
    return redirect(url_for('error403'))


@app.route('/403')
def error403():
    context = {'title': 'Ошибка 403', 'answer': 'доступ к запрашиваемой странице запрещен'}
    return render_template('403.html', **context)


if __name__ == '__main__':
    app.run(debug=True)

