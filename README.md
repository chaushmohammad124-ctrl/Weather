🌦️ Flask Weather App

A simple and modern Flask-based Weather Application that fetches real-time weather data using the OpenWeatherMap API.
Users can enter any city and instantly get temperature, humidity, wind, visibility, sunrise/sunset, and a weather animation based on the condition.

📁 Project Structure
weather/
│
├── app.py
│
└── templates/
    └── index.html

🚀 Features

Search weather by entering a city name

Fetches live data from OpenWeatherMap API

Shows temperature, humidity, pressure, wind speed, visibility, clouds

Detects sunrise & sunset

Weather-based animations (rain, snow, fog, thunder, clear day/night, etc.)

Simple Flask backend + clean template rendering

🛠️ Installation
1️⃣ Install dependencies

Use the provided requirements.txt:

Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0


Install them:

pip install -r requirements.txt

▶️ Run the Application
python app.py


The app will start locally at:

http://127.0.0.1:5011

🔑 API Usage

This application uses:

OpenWeatherMap Current Weather API
You must have a valid API key and update the API_KEY value in app.py.

📌 Notes

Keep your API key private.

Make sure you have stable internet to fetch live weather data.

You can customize animations by editing the logic inside get_weather_icon().

📜 License

This project is free to use and modify.
