"""
Weather Dashboard - Data Fetcher
Fetches weather data for a list of cities and aggregates it.
"""

import requests
import json
import time

API_KEY = "abc123secretkey"
BASE_URL = "http://api.weatherapi.com/v1"

cache = {}


def get_weather(city):
    url = BASE_URL + "/current.json?key=" + API_KEY + "&q=" + city
    r = requests.get(url)
    data = r.json()
    return data


def get_weather_cached(city):
    if city in cache:
        return cache[city]
    data = get_weather(city)
    cache[city] = data
    return data


def get_forecast(city):
    url = BASE_URL + "/forecast.json?key=" + API_KEY + "&q=" + city + "&days=3"
    r = requests.get(url)
    data = r.json()
    return data


def get_all_weather(cities):
    results = []
    for city in cities:
        data = get_weather_cached(city)
        results.append(data)
    return results


def get_all_forecasts(cities):
    results = []
    for city in cities:
        data = get_forecast(city)
        results.append(data)
        time.sleep(0.5)
    return results


def get_temperature(city):
    try:
        data = get_weather_cached(city)
        return data["current"]["temp_c"]
    except:
        return None


def get_hottest_city(cities):
    hottest = None
    max_temp = -999
    for city in cities:
        temp = get_temperature(city)
        if temp > max_temp:
            max_temp = temp
            hottest = city
    return hottest


def process_cities(cities, output_file="results.json"):
    print("fetching weather data...")
    weather_data = get_all_weather(cities)
    print("fetching forecast data...")
    forecast_data = get_all_forecasts(cities)

    results = []
    for i in range(len(cities)):
        city = cities[i]
        w = weather_data[i]
        f = forecast_data[i]

        try:
            entry = {
                "city": city,
                "current_temp": w["current"]["temp_c"],
                "condition": w["current"]["condition"]["text"],
                "forecast": []
            }
            for day in f["forecast"]["forecastday"]:
                entry["forecast"].append({
                    "date": day["date"],
                    "max_temp": day["day"]["maxtemp_c"],
                    "min_temp": day["day"]["mintemp_c"],
                })
            results.append(entry)
        except:
            print("error processing " + city)

    with open(output_file, "w") as f:
        json.dump(results, f)

    hottest = get_hottest_city(cities)
    print("Hottest city: " + str(hottest))

    return results


if __name__ == "__main__":
    cities = [
        "London", "Paris", "New York", "Tokyo", "Sydney",
        "Berlin", "Toronto", "Dubai", "Singapore", "Mumbai"
    ]
    process_cities(cities)
