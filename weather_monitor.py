import requests
import os
from dotenv import load_dotenv
import schedule
import time
import sqlite3
import smtplib
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# Load environment variables
load_dotenv()

# SQLite setup to store daily summaries
conn = sqlite3.connect('weather_data.db')
c = conn.cursor()

# Create the weather table if it doesn't already exist
c.execute('''CREATE TABLE IF NOT EXISTS weather
             (date TEXT, city TEXT, avg_temp REAL, max_temp REAL, min_temp REAL, condition TEXT)''')

# API call to get weather data
def get_weather_data(city):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    API_KEY = os.getenv('OPENWEATHER_API_KEY')

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    print(f"Fetching 5-day forecast for {city}")
    start_time = time.time()

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        end_time = time.time()
        print(f"Operation took {end_time - start_time} seconds")

        print(f"Response Status: {response.status_code}")
        weather_data = response.json()
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        return weather_data, humidity, wind_speed

    except requests.exceptions.RequestException as e:
        print(f"Failed to get weather data: {e}")
        return None, None, None


# Store daily summary into SQLite database
def store_daily_summary(date, city, avg_temp, max_temp, min_temp, condition,humidity, wind_speed):
    c.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?)",
              (date, city, avg_temp, max_temp, min_temp, condition,humidity, wind_speed))
    conn.commit()

# List of cities to track
cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]

# Dictionary to store daily summaries per city
daily_summaries = defaultdict(list)

# Calculate daily aggregate for each city
def calculate_daily_aggregate():
    for date, records in daily_summaries.items():
        for city in cities:
            city_records = [record for record in records if record[0] == city]
            
            if city_records:
                temps = [record[1] for record in city_records]
                avg_temp = sum(temps) / len(temps)
                max_temp = max(temps)
                min_temp = min(temps)
                
                # You can also calculate dominant weather condition if needed.
                conditions = [record[2] for record in city_records]
                dominant_condition = max(set(conditions), key=conditions.count)
                
                print(f"Date: {date}, City: {city}, Avg Temp: {avg_temp}, Max Temp: {max_temp}, Min Temp: {min_temp}, Dominant Condition: {dominant_condition}")


temp_threshold = 35  # Example threshold

def check_alert(weather_data):
    temp = weather_data['main']['temp']
    if temp > temp_threshold:
        trigger_alert(weather_data)

def trigger_alert(weather_data):
    print(f"Alert: Temperature in {weather_data['name']} is {weather_data['main']['temp']}°C")

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

# Visualize weather trends using matplotlib
def plot_temperature_trends(city):
    query = f"SELECT date, avg_temp FROM weather WHERE city='{city}' ORDER BY date"
    c.execute(query)
    data = c.fetchall()

    if data:
        dates, avg_temps = zip(*data)  # Unzip the date and avg_temp
        plt.plot(dates, avg_temps, marker='o', label=city)

# Call this function after you have aggregated data
for city in cities:
    plot_temperature_trends(city)

plt.xlabel('Date')
plt.ylabel('Average Temperature (°C)')
plt.title('Daily Average Temperatures for Cities')
plt.legend()
plt.show()


# Job to fetch weather data and store it
def job():
    for city in cities:
        # Fetch current weather data
        weather_data, humidity, wind_speed = get_weather_data(city)

        if weather_data:
            temp = weather_data['main']['temp']
            condition = weather_data['weather'][0]['description']
            date = time.strftime("%Y-%m-%d")  # Today's date

            if date not in daily_summaries:
                daily_summaries[date] = []

            # Store the current weather data in the daily summary
            daily_summaries[date].append((city, temp, condition, humidity, wind_speed))
            print(f"Stored weather data for {city} on {date}: {temp}°C, {condition}, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s")

            # Store the current weather data in the database
            store_daily_summary(date, city, temp, temp, temp, condition, humidity, wind_speed)

        # Fetch 5-day weather forecast data
        forecast_data = get_weather_data(city)
        if forecast_data:
            store_forecast_data(forecast_data, city)

    # Calculate and store daily aggregates (can be done periodically or at the end of the day)
    calculate_daily_aggregate()


# Schedule the job to run every hour (adjust as needed)
schedule.every().hour.do(job)

def store_forecast_data(forecast_data, city):
    for forecast in forecast_data['list']:
        temp = forecast['main']['temp']
        condition = forecast['weather'][0]['description']
        humidity = forecast['main']['humidity']
        wind_speed = forecast['wind']['speed']
        date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
        
        # Store the forecast in the database
        store_daily_summary(date, city, temp, temp, temp, condition, humidity, wind_speed)
        print(f"Stored forecast data for {city} on {date}: {temp}°C, {condition}, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s")


# Main loop to run the scheduler
if __name__ == "__main__":
    print("Starting the operation...")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Close SQLite connection when no longer needed
conn.close()
