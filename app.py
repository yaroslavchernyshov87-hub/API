from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Страница с инфой о стране
@app.route('/result', methods=['POST'])
def result():
    country = request.form['country']

    try:
        url = f"https://restcountries.com/v3.1/name/{country}"
        response = requests.get(url)
        data = response.json()[0]

        name = data['name']['common']
        capital = data['capital'][0]
        population = data['population']
        region = data['region']
        flag = data['flags']['png']

        lat = data['latlng'][0]
        lon = data['latlng'][1]

        # логика
        if population > 50000000:
            size = "🌍 Dette er et stort land"
        else:
            size = "🌱 Dette er et lite land"

        return render_template(
            'result.html',
            name=name,
            capital=capital,
            population=population,
            region=region,
            flag=flag,
            size=size,
            lat=lat,
            lon=lon
        )

    except:
        return render_template('error.html')


# Страница с погодой (второй API)
@app.route('/weather/<lat>/<lon>')
def weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        data = response.json()

        temp = data['current_weather']['temperature']
        wind = data['current_weather']['windspeed']

        if temp > 20:
            message = "☀️ Det er varmt!"
        else:
            message = "❄️ Det er kaldt!"

        return render_template(
            'weather.html',
            temp=temp,
            wind=wind,
            message=message
        )

    except:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)