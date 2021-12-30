from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class EditForm(FlaskForm):
    name = StringField('Имя', validators=[InputRequired(), Length(min=2)])
    surname = StringField('Фамилия', validators=[InputRequired(), Length(min=2)])
    midname = StringField('Отчество', validators=[InputRequired(), Length(min=2)])
    username = StringField('Логин', validators=[InputRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[InputRequired(), Length(min=2)])
    phone = StringField('Телефон', validators=[InputRequired(), Length(min=2)])
    lvl = StringField('Уровень пользователя', validators=[InputRequired(), Length(min=0)])


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[InputRequired(), Length(min=2)])
    surname = StringField('Фамилия', validators=[InputRequired(), Length(min=2)])
    midname = StringField('Отчество', validators=[InputRequired(), Length(min=2)])
    email = StringField('Email', validators=[Length(min=0)])
    phone = StringField('Телефон', validators=[Length(min=0)])
    username = StringField('Логин', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=8, max=80)])


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[InputRequired(), Length(min=4, max=30)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Запомнить меня')


class AddForm(FlaskForm):
    name = StringField('Имя', validators=[InputRequired(), Length(min=2)])
    surname = StringField('Фамилия', validators=[InputRequired(), Length(min=2)])
    midname = StringField('Отчество', validators=[InputRequired(), Length(min=2)])
    username = StringField('Логин', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=6, max=80)])
    phone = StringField('Номер телефона', validators=[Length(min=0, max=30)])
    email = StringField('Email', validators=[Length(min=0, max=50)])
