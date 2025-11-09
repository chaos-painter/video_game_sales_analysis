import requests
import os
import time
from prometheus_client import start_http_server, Gauge
from threading import Thread

API_KEY = os.getenv('OPENWEATHER_API_KEY', '21df615d9232c9a3bd548e5ec53fc461')
city = os.getenv('city', 'Moscow')
BASE_URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# 12 Gauges for metrics
cities = 'Moscow,London,New York,Tokyo,Berlin,Paris,Sydney,Singapore,Dubai,San Francisco'.split(',')
# Create metrics per city with a label 'city'
metrics = {
    'temperature': Gauge('weather_temperature_celsius', 'Current temperature in Celsius', ['city']),
    'feels_like': Gauge('weather_feels_like_celsius', 'Feels like temperature in Celsius', ['city']),
    'temp_min': Gauge('weather_temp_min_celsius', 'Minimum temperature in Celsius', ['city']),
    'temp_max': Gauge('weather_temp_max_celsius', 'Maximum temperature in Celsius', ['city']),
    'pressure': Gauge('weather_pressure_hpa', 'Atmospheric pressure in hPa', ['city']),
    'humidity': Gauge('weather_humidity_percent', 'Humidity in percent', ['city']),
    'wind_speed': Gauge('weather_wind_speed_mps', 'Wind speed in m/s', ['city']),
    'wind_deg': Gauge('weather_wind_degrees', 'Wind direction in degrees', ['city']),
    'clouds': Gauge('weather_clouds_percent', 'Cloud percentage', ['city']),
    'visibility': Gauge('weather_visibility_meters', 'Visibility in meters', ['city']),
    'rain_1h': Gauge('weather_rain_mm_1h', 'Rain volume in last 1h in mm', ['city']),
    'snow_1h': Gauge('weather_snow_mm_1h', 'Snow volume in last 1h in mm', ['city']),
    'sunrise': Gauge('weather_sunrise_timestamp', 'Sunrise Unix timestamp', ['city']),
    'sunset': Gauge('weather_sunset_timestamp', 'Sunset Unix timestamp', ['city']),
}

def fetch_weather():
    while True:
        for city in cities:
            try:
                BASE_URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                resp = requests.get(BASE_URL, timeout=10)
                resp.raise_for_status()
                data = resp.json()

                main = data['main']
                metrics['temperature'].labels(city=city).set(main['temp'])
                metrics['feels_like'].labels(city=city).set(main['feels_like'])
                metrics['temp_min'].labels(city=city).set(main['temp_min'])
                metrics['temp_max'].labels(city=city).set(main['temp_max'])
                metrics['pressure'].labels(city=city).set(main['pressure'])
                metrics['humidity'].labels(city=city).set(main['humidity'])

                wind = data['wind']
                metrics['wind_speed'].labels(city=city).set(wind['speed'])
                metrics['wind_deg'].labels(city=city).set(wind.get('deg', 0))

                metrics['clouds'].labels(city=city).set(data['clouds']['all'])
                metrics['visibility'].labels(city=city).set(data.get('visibility', 0))

                metrics['rain_1h'].labels(city=city).set(data.get('rain', {}).get('1h', 0))
                metrics['snow_1h'].labels(city=city).set(data.get('snow', {}).get('1h', 0))

                sys_info = data['sys']
                metrics['sunrise'].labels(city=city).set(sys_info['sunrise'])
                metrics['sunset'].labels(city=city).set(sys_info['sunset'])

                print(f"Fetched weather for {city}: Temp={main['temp']}°C")
            except Exception as e:
                print(f"Error fetching weather for {city}: {e}")
                for gauge in metrics.values():
                    gauge.labels(city=city).set(0)

        time.sleep(20)

if __name__ == '__main__':
    print(f"Starting Custom Exporter for {city} on port 8000")
    start_http_server(8000)
    Thread(target=fetch_weather, daemon=True).start()
    while True:
        time.sleep(1)  # Keep main thread alive