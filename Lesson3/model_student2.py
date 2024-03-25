from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Students2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    group_ = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    # Связь one-to-many студент - его оценки
    student_grade = db.relationship('Grades', backref='link', lazy=True)


class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students2.id'), nullable=False)
    name_subject = db.Column(db.String(15), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
