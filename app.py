import requests
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/api/hello', methods=["GET"])
def home():
    """
    This function returns the client's IP address, location, and city after receiving query parameters from the URL.
    Real-time data is gathered using Weatherapi.
    """
    name = request.args.get('visitor_name').strip('"').title()
    
    api_key = os.getenv("API_KEY")
    
    temperature_endpoint = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q=auto:ip"
    ip_endpoint = f"https://api.weatherapi.com/v1/ip.json?key={api_key}&q=auto:ip"
    
    temp_data = requests.get(temperature_endpoint).json()
    ip_data = requests.get(ip_endpoint).json()
        

    ip_address = ip_data["ip"]
    city = ip_data["city"].title()
    temp = temp_data["current"]["temp_c"]
    
    
    response = {
        "client_ip" : f"{ip_address}",
        "location" : f"{city}",
        "greeting": f"Hello, {name}!, The temperature is {temp} degrees celsius in {city}",
    }
    
    return jsonify(response)
   

    