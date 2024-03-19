# Написать функцию, которая будет принимать на вход два числа и выводить на экран их сумму

from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/sum/<int:a>/<int:b>/')
def what_sum(a=0, b=0):
    return f'Сумма чисел: {a} и {b} - это {a + b}'
