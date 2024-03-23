# Создать страницу, на которой будет изображение и ссылка на другую страницу,
# на которой будет отображаться форма для загрузки изображений.
from pathlib import Path, PurePath

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    context = {'title': 'Загрузка файла', 'url': 'submit', 'name_button': 'Загрузить изображение'}
    return render_template('index.html', **context)


@app.route('/submit/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'static/uploads', file_name))
        context = {'title': 'Загрузка завершена', 'answer': f'Файл {file_name} загружен'}
        return render_template('answer.html', **context)
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)

