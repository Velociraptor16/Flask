from flask import Flask, request
from faker import Faker
import csv
import requests

app = Flask(__name__)
fake = Faker()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/requirements/')
def requirements():
    with open('requirements.txt', 'r', encoding='UTF-8') as text:
        return text.read()


@app.route('/generate-users/')
def user_generate():
    value = request.args.get('count', 100)
    handbook = {}
    for _ in range(int(value)):
        person = {fake.name(): fake.email()}
        handbook.update(person)
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
    return f'Average weight in Kg: {weight_kg} ' \
           f'Average height in CM:{height_cm}'


@app.route('/space/')
def astronaut():
    response = requests.get('http://api.open-notify.org/astros.json')
    number = response.json()['number']
    return f'{str(number)} astronauts are in space now'


if __name__ == '__main__':
    app.run()
