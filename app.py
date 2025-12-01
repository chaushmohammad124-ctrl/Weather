from flask import Flask, render_template, request, jsonify
import requests
import datetime
from typing import Dict, Any
import os

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = ""  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_icon(weather_id: int, is_day: bool = True) -> str:
    """Convert weather condition code to icon class"""
    if 200 <= weather_id <= 232:
        return "thunder"
    elif 300 <= weather_id <= 321:
        return "drizzle"
    elif 500 <= weather_id <= 531:
        return "rain"
    elif 600 <= weather_id <= 622:
        return "snow"
    elif 701 <= weather_id <= 781:
        return "fog"
    elif weather_id == 800:
        return "clear" if is_day else "clear-night"
    elif 801 <= weather_id <= 804:
        return "clouds"
    else:
        return "clear"

def get_weather_data(city: str) -> Dict[str, Any]:
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'en'
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Calculate if it's daytime
        current_time = datetime.datetime.utcnow().timestamp()
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        is_day = sunrise <= current_time <= sunset
        
        # Get weather animation type
        weather_id = data['weather'][0]['id']
        animation_type = get_weather_icon(weather_id, is_day)
        
        return {
            'success': True,
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind'].get('deg', 0),
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'animation_type': animation_type,
            'visibility': data.get('visibility', 0) / 1000 if data.get('visibility') else 0,
            'cloudiness': data['clouds']['all'],
            'is_day': is_day,
            'sunrise': datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        }
    
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f"Error fetching weather data: {str(e)}"
        }
    except KeyError as e:
        return {
            'success': False,
            'error': f"Invalid data received from weather service"
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city', '').strip()
    if not city:
        return jsonify({'success': False, 'error': 'Please enter a city name'})
    
    weather_data = get_weather_data(city)
    return jsonify(weather_data)

@app.route('/demo/<animation_type>')
def demo_animation(animation_type):
    """Route to demo different weather animations"""
    valid_animations = ['rain', 'snow', 'clear', 'clouds', 'thunder', 'drizzle', 'fog', 'clear-night']
    if animation_type not in valid_animations:
        animation_type = 'clear'
    
    demo_data = {
        'success': True,
        'city': 'Demo City',
        'country': 'DC',
        'temperature': 22,
        'feels_like': 24,
        'humidity': 65,
        'pressure': 1013,
        'wind_speed': 3.5,
        'description': f'{animation_type.title()} Demo',
        'animation_type': animation_type,
        'visibility': 10,
        'cloudiness': 20,
        'is_day': animation_type != 'clear-night',
        'sunrise': '06:30',
        'sunset': '18:45'
    }
    
    return render_template('index.html', weather=demo_data)

if __name__ == '__main__':

    app.run(debug=True, port=5011)
