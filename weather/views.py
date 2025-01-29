from django.shortcuts import render

import os
import requests
from django.shortcuts import render
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

def home(request):
    weather_data = {}
    error = None
    
    if request.method == 'POST':
        city = request.POST.get('city', 'London')
        API_KEY = os.getenv('OPENWEATHER_API_KEY')
        
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            weather_data = {
                'city': data['name'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
            }
            
        except requests.exceptions.RequestException as e:
            error = "City not found. Please try again."
    
    return render(request, 'weather/index.html', {
        'weather': weather_data,
        'error': error
    })

def get_weather_data(city):
    api_key = settings.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def index(request):
    city = request.GET.get('city', 'default_city')  # Replace 'default_city' with a default value
    weather_data = get_weather_data(city)
    print(weather_data)  # Debugging: print the response to the console
    return render(request, 'weather/index.html', {'weather_data': weather_data}) 
