import requests


test_lat = 64.14


test_lon = -21.92


weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={test_lat}&longitude={test_lon}&current=cloud_cover"






print(f"Scanning the skies at Lat: {test_lat}, Lon: {test_lon}...")
response = requests.get(weather_url).json()

cloud_cover = response["current"]['cloud_cover']


print(f"Current Cloud Cover: {cloud_cover}%")


if cloud_cover < 30:
    print("Skies are clear! Perfect for astrophotography.")
else:
    print("Too cloudy. The aurora is blocked.")












