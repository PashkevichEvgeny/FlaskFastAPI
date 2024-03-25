# Создать форму регистрации для пользователя.
# Форма должна содержать поля: имя,
#                              электронная почта,
#                              пароль (с подтверждением),
#                              дата рождения,
#                              согласие на обработку персональных данных.
# Валидация должна проверять, что все поля заполнены корректно (дата рождения должна быть в формате дд.мм.гггг).
# При успешной регистрации пользователь должен быть перенаправлен на страницу подтверждения регистрации.

form_data = []

from flask import Flask, request, render_template, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from Lesson3.form_user2 import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "mySecretKEY"
csrf = CSRFProtect(app)


@app.route('/')
@app.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        form_data.append(form)
        return render_template('answer.html', **{'answer': 'yes'})
    return render_template('registration.html', form=form)


@app.route('/confirm/')
def confirm():
    return render_template('answer.html', **{'answer': 'confirm', 'username': form_data[0].username.data})
