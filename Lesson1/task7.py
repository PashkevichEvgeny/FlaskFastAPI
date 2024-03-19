# Написать функцию, которая будет выводить на экран HTML страницу с блоками новостей.
# Каждый блок должен содержать заголовок новости, краткое описание и дату публикации.
# Данные о новостях должны быть переданы в шаблон через контекст
import csv
import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return '<a href="index">Hello!</a></br> ' \
           '<a href="news"><h1>НОВОСТИ</h1></a>'


@app.route('/index/')
def html_index():
    return render_template('index.html')


@app.route('/news/')
def html_table():
    news = []
    with open(r'/Lesson1/static/news/news.csv', 'r', encoding='UTF-8') as f:
        for n in f.readlines():
            title, review = n.split('|')
            news.append({'title': title, 'review': review, 'date': datetime.datetime.now().strftime('%d-%m-%y')})
    context = {'news': news}
    return render_template('news.html', **context)
