from flask import Flask, request, render_template
from faker import Faker
import csv
import requests

app = Flask(__name__)
fake = Faker()


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/requirements/')
def requirements():
    with open('requirements.txt', 'r', encoding='UTF-8') as text:
        lst = text.readlines()
        lines = tuple(map(lambda value: value.strip('\n'), lst))
        return render_template('parameters.html', line=lines)


@app.route('/generate-users/')
def user_generate():
    value = request.args.get('count', 100)
    handbook = {}
    template_name = '{name:<20}'
    template_email = '{email:<15}'
    for _ in range(int(value)):
        person = fake.name()
        email = fake.email()
        line = {template_name.format(name=person): template_email.format(email=email)}
        handbook.update(line)
    return handbook


@app.route('/mean/')
def parameters():
    with open('hw.csv', newline='') as csvfile:
        lines = csv.reader(csvfile.readlines()[1:25001], delimiter=',')
        height_inches = 0
        weight_pounds = 0
        for row in lines:
            height_inches += float(row[1])
            weight_pounds += float(row[2])
        height_cm = round(height_inches * 2.54, 2)
        weight_kg = round(weight_pounds / 2.2046, 2)
    return render_template('parameters.html', weight=weight_kg, height=height_cm)


@app.route('/space/')
def astronaut():
    response = requests.get('http://api.open-notify.org/astros.json')
    number = response.json()['number']
    return render_template('parameters.html', number=number)


if __name__ == '__main__':
    app.run()
