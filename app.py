from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
api_details = {
    'api_key': os.getenv('API_KEY'),
    'api_url': os.getenv('API_URL')
}

app = Flask(__name__)

def kelvin_to_celsius(kelvin):
    return f"{round(kelvin - 273.15)}°C"

def format_time(unix_timestamp, timezone_offset, time_only=False):
    timezone_offset = int(timezone_offset)
    local_time = datetime.utcfromtimestamp(unix_timestamp + timezone_offset)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/weather-app', methods=['POST'])
def getWeatherData():
    city = request.form.get('city')
    if not city:
        return render_template('error.html', error='City not provided.')

    try:
        response = requests.get(api_details['api_url'].format(city, api_details['api_key']))
        if response.status_code != 200:
            return render_template('error.html', error=f"Error: {response.status_code}. Unable to fetch data.")

        result = response.json()
        result = response.json()
        
        if not all(key in result for key in ('main', 'weather', 'dt', 'timezone', 'name', 'sys', 'wind')):
            return render_template('error.html', error='Incomplete data received from the API.')
        
        weather = {
            "city": city,
            "temperature": kelvin_to_celsius(result["main"]["temp"]),
            "icon" : f"http://openweathermap.org/img/wn/{result['weather'][0]['icon']}.png",
            "description": result["weather"][0]["description"].capitalize(),
            "date": format_time(result["dt"], result["timezone"]).split()[0],
            "day_time": format_time(result["dt"], result["timezone"]).split()[1],
            "time_of_day": "Day" if result["weather"][0]["icon"].endswith("d") else "Night",
            "location": f"{result['name']}, {result['sys']['country']}",
            "additional_info": [
                {"title": "Wind", "value": f"{round(result['wind']['speed'] * 3.6, 1)} km/h, {result['wind']['deg']}°"},
                {"title": "Humidity", "value": f"{result['main']['humidity']}%"},
                {"title": "Real Feel", "value": kelvin_to_celsius(result["main"]["feels_like"])},
                {"title": "Pressure", "value": f"{result['main']['pressure']} mb"},
                {"title": "Temperature History", "value": f"Max: {kelvin_to_celsius(result['main']['temp_max'])}, Min: {kelvin_to_celsius(result['main']['temp_min'])}"},
                {"title": "Sunrise", "value": format_time(result['sys']['sunrise'], result['timezone'], time_only=True)},
                {"title": "Sunset", "value": format_time(result['sys']['sunset'], result['timezone'], time_only=True)}
            ]
        }
        return render_template('mainpage.html', weather=weather, city=city)
        
    except Exception as e:
        return render_template('error.html', error=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
