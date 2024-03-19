# Написать функцию, которая будет принимать на вход строку и выводить на экран ее длину.

from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/<string>')
def what_sum(string=''):
    return f'Длина введенной строки {string} равна {len(string)}'
