import os
import requests
from dotenv import load_dotenv

# load the api key from the .env file
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")


# simple class to store the weather info
class Weather:
    def __init__(self, city, description, temp, humidity):
        self.city = city
        self.description = description
        self.temp = temp
        self.humidity = humidity

    def show_summary(self):
        print(f"\nWeather in {self.city}:")
        print(f"- Condition: {self.description}")
        print(f"- Temperature: {self.temp} C")
        print(f"- Humidity: {self.humidity}%")


# function to get data from the weather API
def get_weather(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    
    # check if the request worked
    if response.status_code == 200:
        data = response.json()
        
        # pull the data we need from json
        city = data["name"]
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        
        # save it in our class and return it
        weather_obj = Weather(city, desc, temp, humidity)
        return weather_obj
    else:
        print("Error: Could not get weather data. Check your API key.")
        return None


# run the program
if __name__ == "__main__":
    if not api_key:
        print("Please add your API key in the .env file first!")
    else:
        my_weather = get_weather("Cairo")
        if my_weather:
            my_weather.show_summary()
