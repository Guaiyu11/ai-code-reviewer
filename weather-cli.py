#!/usr/bin/env python3
"""
Weather CLI - Get current weather for a city.
Usage: python weather-cli.py <city> [--unit C|F]
"""

import sys
import urllib.request
import json

def get_weather(city, unit='C'):
    """Get weather using wttr.in (free, no API key)."""
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
        
        current = data['current_condition'][0]
        temp_C = current['temp_C']
        temp_F = current['temp_F']
        desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind = current['windspeedKmph']
        
        return {
            'city': city,
            'temp_C': temp_C,
            'temp_F': temp_F,
            'description': desc,
            'humidity': humidity,
            'wind_kmh': wind,
        }
    except Exception as e:
        return None, str(e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python weather-cli.py <city> [--unit C|F]")
        sys.exit(1)
    
    city = sys.argv[1]
    unit = 'C'
    
    for arg in sys.argv:
        if arg == '--unit' and len(sys.argv) > 1:
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                unit = sys.argv[idx + 1].upper()
    
    result, error = get_weather(city, unit)
    
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    temp = result['temp_C'] + '°C' if unit == 'C' else result['temp_F'] + '°F'
    
    print(f"=== Weather: {result['city']} ===\n")
    print(f"Temperature: {temp}")
    print(f"Condition:   {result['description']}")
    print(f"Humidity:    {result['humidity']}%")
    print(f"Wind:        {result['wind_kmh']} km/h")
