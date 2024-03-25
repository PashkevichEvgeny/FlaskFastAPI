# Создать форму для регистрации пользователей на сайте.
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

from os import urandom
from hashlib import pbkdf2_hmac

from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from Lesson3.form_user4 import RegistrationForm
from Lesson3.model_user2 import db, User2

app = Flask(__name__)
app.config['SECRET_KEY'] = "mySecretKEY"
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    print('Таблицы созданы')


@app.route('/')
@app.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        lastname = form.lastname.data
        email = form.email.data
        salt = urandom(32)
        password = hash_salt_password(form.password.data, salt)
        user = User2(name=name, lastname=lastname, email=email, password=password, salt=salt)
        db.session.add(user)
        db.session.commit()
        context = {
            'answer': f'Регистрация успешно завершена {name}!'}
        return render_template('answer.html', **context)
    return render_template('registration.html', form=form)


def hash_salt_password(password, salt):
    return pbkdf2_hmac('sha256',  # Используемый алгоритм хеширования
                       password.encode('utf-8'),  # Конвертирование пароля в байты
                       salt,  # Предоставление соли
                       100000,  # Рекомендуется использоваться по крайней мере 100000 итераций SHA-256
                       dklen=128)  # Получает ключ в 128 байтов
