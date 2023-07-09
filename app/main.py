import os
import smtplib
from email.mime.text import MIMEText

import joblib
import pandas as pd
from wtforms import SelectField, FloatField, StringField, EmailField, TextAreaField
from flask import Flask, abort, render_template, flash, url_for, redirect
from wtforms.validators import DataRequired, AnyOf, NumberRange
from flask_wtf import FlaskForm
from dotenv import load_dotenv


load_dotenv()
model = joblib.load('models/xgb_v1.joblib')

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'


@app.route('/badrequest400')
def bad_request():
    return abort(400)


app.config.update(dict(
    SECRET_KEY="h34hs893h23sd23",
    WTF_CSRF_SECRET_KEY="jk543hoj534j534kl342ly"
))


class MyForm(FlaskForm):
    cities = pd.read_csv("data/location.csv").Location.values.tolist()
    city = StringField('City', validators=[DataRequired(), AnyOf(values=cities, message='Такого населеного пункту не знайдено')])
    area = FloatField('Area', validators=[DataRequired(message='Поле «площа» заповнено некоректно'), NumberRange(min=None, max=500, message='Занадто велика площа!'), NumberRange(min=10, max=None, message='Занадто мала площа!')])
    rooms = SelectField('Rooms', validators=[DataRequired()],
                        choices=[('', 'Кімнатність'), (1, '1 кімната'), (2, '2 кімнати'), (3, '3 кімнати'),
                                 (4, '4 кімнати'), (5, '5+ кімнат')], option_widget=None, validate_choice=True)
    floor = SelectField('Floor', validators=[DataRequired()], choices=[('', 'Поверх'),
                                                                       ('First', 'Перший поверх'),
                                                                       ('Last', 'Останній поверх'),
                                                                       ('Middle', 'Не перший & не останній поверх')])


@app.route('/', methods=('GET', 'POST'))
def main_page():
    form = MyForm()
    cities = pd.read_csv("data/location.csv").Location.values.tolist()
    if form.validate_on_submit():

        df = pd.read_csv("data/location.csv")
        city = df[df.Location == form.city.data]['Normalized'].iloc[0]
        city_reg = city.split(' ')
        city = city_reg[1]
        region = city_reg[0]

        area = form.area.data
        rooms = form.rooms.data
        floor = form.floor.data

        data = {'Region': region, 'City': city, 'Floor': floor, 'Area': area, 'Rooms': rooms}
        df = pd.DataFrame(data=data, index=['1'])

        predicted_value = round(model.predict(df)[0])
        full_price = '{0:,}'.format(round(predicted_value * area)).replace(',', ' ')
        predicted_value = '{0:,}'.format(predicted_value).replace(',', ' ')

        return render_template('index.html', form=form, predicted_value=str(predicted_value), full_price=str(full_price), cities=cities)
    return render_template('index.html', form=form, cities=cities)


@app.route('/about')
def about():
    return render_template('about.html')


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])


def send_feedback(name, email, text):
    sender = "bohdan1404@gmail.com"
    password = os.getenv('PASSWORD_EMAIL_APP')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    html_template = f"""
    <!doctype html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
    </head>
    <body>
        <h4>From: {name} | {email}</h4>
        <p>{text}</p>
    </body>
    </html>
    """

    try:
        server.login(sender, password)
        msg = MIMEText(html_template, "html")
        msg['Subject'] = 'Message from the feedback form'
        server.sendmail(sender, sender, msg.as_string())
        return 'The message has been sent'
    except (Exception, ) as e:
        print(e)
        return "Message wasn't sent"


@app.route('/feedback', methods=('GET', 'POST'))
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        text = form.text.data
        send_feedback(name, email, text)
        flash(message='Дякую, повідомлення надіслано!', category='message')

        return redirect(url_for('feedback'))

    return render_template('feedback.html', form=form)
