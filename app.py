import requests
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)


def get_data(ip_address):
    api_key = os.getenv("API_KEY")
    
    weather_endpoint = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={ip_address}"
    
    weather_data = requests.get(weather_endpoint).json()

    city = weather_data["location"]["name"]
    temperature = weather_data["current"]["temp_c"]
    
    data = {
        "location" : city,
        "temperature" : temperature,
    }
    
    
    return data


@app.route('/api/hello', methods=["GET"])
def home():
    """
    This function returns the client's IP address, location, and city after receiving query parameters from the URL.
    Real-time data is gathered using Weatherapi.
    """
    

    name = request.args.get('visitor_name').strip('"').title()
    
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        client_ip = request.remote_addr
        
    current_data = get_data(client_ip)
    response = {
        "client" : client_ip,
        "location" : current_data.get("location"),
        "greeting" : f"Hello, {name}!, The temperature is {current_data.get("temperature")} in {current_data.get("location")}"
    }
    
    return response














    
    # ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        client_ip = request.remote_addr
    
    # current_data = get_data(client_ip)
    # response = {
    #     "client" : client_ip,
    #     "location" : current_data.get("location"),
    #     "greeting" : f"Hello, {name}!, The temperature is {current_data.get("temperature")} in {current_data.get("location")}"
    # }
    
    # return response
    # return current_data
    
    


        
        

   

    