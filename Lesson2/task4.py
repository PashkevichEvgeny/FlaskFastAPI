# Создать страницу, на которой будет форма для ввода текста и кнопка "Отправить"
# При нажатии кнопки будет произведен подсчет количества слов в тексте и переход на страницу с результатом.

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

count_words = {'count': ''}


@app.route('/')
@app.get('/submit')
def get():
    context = {'name_button': 'Отправить текст'}
    return render_template('textarea.html', **context)


@app.post('/submit/')
def post():
    length_list = len(request.form.get('name').split())
    count_words['count'] = f'Количество слов: {length_list}'
    return redirect(url_for('count_word'))


@app.route('/count-word/')
def count_word():
    context = {'title': 'Количество слов', 'answer': count_words['count']}
    return render_template('answer.html', **context)


if __name__ == '__main__':
    app.run(debug=True)