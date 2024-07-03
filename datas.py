from flask import Flask,request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

def get_location():
    """
    The function gets the client's ip address, and uses ipapi to get the clients exact location using latitude and longitude
    coordinates. The, data returned is formatted to JSON, put in a dictionary and returned.
    """
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    url = f"https://ipapi.co/{client_ip}/json/"
    
    url_data = requests.get(url).json()
    
    coordinates = {
        "lat" : url_data["latitude"],
        "lon": url_data["longitude"],
        "ip": client_ip
        }
    return coordinates
    

@app.route('/api/hello')
def get_client_data():
    """
    The function retrieves the name from the query parameter. OpenWeatherMap is used to get current weather data of the client's
    location.
    """
    api_key = os.getenv("API_KEY")
    
    name = request.args.get('visitor_name').strip('"').title()
        
    location_coord = get_location()
    
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={location_coord['lat']}&lon={location_coord['lon']}&units=metric&appid={api_key}"

    weather_data = requests.get(weather_url).json()
    
    city = weather_data["name"]
    temperature = str(weather_data["main"]["temp"])
    
    response = {
        "client_ip": location_coord["ip"],
        "location" : city,
        "greeting": f"Hello, {name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    
    return response