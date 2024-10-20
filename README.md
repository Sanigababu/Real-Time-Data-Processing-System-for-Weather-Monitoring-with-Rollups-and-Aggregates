# Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates

## Project Overview

This project is a real-time data processing system that fetches weather data from the OpenWeatherMap API for multiple cities, computes daily summaries (average temperature, minimum and maximum temperatures, and dominant weather conditions), and stores the data in an SQLite database. It also supports additional weather parameters such as humidity and wind speed, and includes 5-day weather forecasts.

### Key Features
- Fetch real-time weather data for multiple cities.
- Convert temperatures from Kelvin to Celsius and Fahrenheit.
- Compute daily summaries such as average temperature and dominant weather condition.
- Support for humidity and wind speed monitoring.
- Configurable alert thresholds for weather conditions.
- 5-day weather forecast with daily summaries.
- Plots temperature trends over time using matplotlib.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- **Python 3.8+**
- **An API key from OpenWeatherMap**
- **SQLite (comes built-in with Python)**
- **Required Python packages can be installed via the following requirements.txt**

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Sanigababu/Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates.git
```
2. **Navigate to the project directory:**

```bash
cd Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates
```
3. **Install dependencies:**

```bash
pip install -r requirements.txt
```
4. **Set up your OpenWeatherMap API key by creating a .env file in the project root and adding:**

```makefile
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage

1. **Start the real-time data processing:**

```bash
python weather_monitor.py
```
The script will automatically fetch weather data for the cities listed in the code, store it in the database, and print daily summaries.

2. **Modify city list:** The cities to be tracked are specified in the cities list within the script. You can modify this list to add or remove cities.

3. **Check daily summaries:** After the data is fetched, the daily summaries for each city are calculated and printed in the console. Data is also stored in the SQLite database (weather_data.db).

## Example API Responses
### Current Weather Data:

```json

{
   "main": {
       "temp": 27.05,
       "humidity": 50
   },
   "wind": {
       "speed": 2.1
   },
   "weather": [{
       "description": "haze"
   }]
}
```

### Forecast Data:

```json

{
   "list": [
       {
           "main": {
               "temp": 28.12,
               "humidity": 52
           },
           "weather": [{
               "description": "cloudy"
           }],
           "wind": {
               "speed": 3.5
           }
       },
       ...
   ]
}
```
### Visualisation
![Screenshot 2024-10-19 104403](https://github.com/user-attachments/assets/44643e7a-4362-42b0-b0a3-3ea2eca6c76e)

## Testing
1. **Test Data Retrieval:** Ensure the system retrieves weather data correctly by running the script. Adjust the scheduling interval to 1 minute for faster testing.
2. **Test Temperature Conversion:** Verify that the temperature is correctly displayed in Celsius (you can add functionality for Fahrenheit).
3.**Test Aggregates:** Confirm that daily summaries are correctly computed, including average temperature and dominant weather condition.
4.**Test Alerts:** Simulate different weather thresholds to check if the alert system is functioning (you can implement alert notifications via email).
   
## Bonus Features
1. **Additional Weather Parameters:** Track humidity and wind speed along with temperature data.
2. **5-Day Weather Forecast:** Fetch and store weather forecast data using the OpenWeatherMap forecast endpoint.
3. **Visualization:** Use matplotlib to generate temperature trend graphs.


