from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, DateField, IntegerField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class AddJobs(FlaskForm):
    job = StringField('Тема', validators=[DataRequired()])
    leader = IntegerField('id руководителя', validators=[DataRequired()])
    work_size = IntegerField('Продолжительность', validators=[DataRequired()])
    collaborators = StringField('id участников', validators=[DataRequired()])
    start = DateField('Начало работ', validators=[DataRequired()])
    end = DateField('Окончание работ', validators=[DataRequired()])
    finish = BooleanField('Завершено?')

    submit = SubmitField('Начать')