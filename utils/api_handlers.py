# api_handlers.py
from pathlib import Path
from dotenv import load_dotenv
import requests
import os
from typing import Optional

env_path = Path(__file__).parent / "environments" / "dev.env"
load_dotenv(env_path)  # Loads from .env file
# --- API Config --- #
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
print(f"Loaded key: {WEATHER_API_KEY}")  # Verify loading

# --- Weather (WeatherAPI.com) --- #
def get_weather(location: str) -> Optional[str]:
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
        print(url)
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            current = data['current']
            location = data['location']
            return (
                f"Weather in {location['name']}, {location['region']}:\n"
                f"• {current['temp_c']}°C ({current['temp_f']}°F)\n"
                f"• Condition: {current['condition']['text']}\n"
                f"• Wind: {current['wind_kph']} km/h\n"
                f"• Humidity: {current['humidity']}%"
            )
        else:
            error = data.get('error', {}).get('message', 'Unknown error')
            return f"Sorry, couldn't fetch weather. {error}"
    
    except Exception as e:
        print(f"WeatherAPI error: {e}")
        return None

# --- News --- #
def get_news(topic: str = "technology") -> Optional[str]:
    try:
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize=1"
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'ok' and data['totalResults'] > 0:
            article = data['articles'][0]
            return f"Latest {topic} news: {article['title']} (Read more: {article['url']})"
        else:
            return "No news found for this topic."
    
    except Exception as e:
        print(f"News API error: {e}")
        return None

# --- Fun Facts --- #
def get_cat_fact() -> Optional[str]:
    try:
        response = requests.get("https://catfact.ninja/fact")
        return response.json().get('fact', "Cats are awesome!")
    except:
        return None
    
# Helper functions
def extract_location(text: str) -> str:
    """Extracts location after 'weather in'"""
    if 'weather in' in text:
        return text.split('weather in')[-1].strip()
    return "London"  # Default

def extract_topic(text: str) -> str:
    """Extracts topic after 'news about'"""
    if 'news about' in text:
        return text.split('news about')[-1].strip()
    return "technology"  # Default    