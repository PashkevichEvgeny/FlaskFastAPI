# Создайте форму регистрации пользователя с использованием Flask-WTF.
# Форма должна содержать следующие поля:
#    Имя пользователя (обязательное поле)
#    Электронная почта (обязательное поле, с валидацией на корректность ввода email)
#    Пароль (обязательное поле, с валидацией на минимальную длину пароля)
#    Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
# После отправки формы данные должны
#    сохраняться в базе данных (можно использовать SQLite)
#    и выводиться сообщение об успешной регистрации.
# Если какое-то из обязательных полей не заполнено или данные не прошли валидацию,
# то должно выводиться соответствующее сообщение об ошибке.
# Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в базе данных.
# Если такой пользователь уже зарегистрирован, то должно выводиться сообщение об ошибке.

from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from Lesson3.form_user import RegistrationForm
from Lesson3.model_user import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "mySecretKEY"
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Таблицы созданы')


@app.route('/')
@app.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        if search_duplicate(username, email):
            return render_template('answer.html', **{'answer': f'Уже {username} - {email} зарегистрован'})
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return render_template('answer.html', **{'answer': f'Регистрация успешно завершена {username}, {email}'})
    return render_template('registration.html', form=form)


def search_duplicate(username, email):
    user = User.query.filter(User.username == username).first()
    email = User.query.filter(User.email == email).first()
    print(user, email)
    if user or email:
        return True
    return False
