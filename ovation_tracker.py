import requests

ovation_url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"

response = requests.get(ovation_url).json()




grid_data = response['coordinates']


print(grid_data)





max_prob = 0
best_lon = 0
best_lat = 0


for point in grid_data:
    lon = point[0]
    lat = point[1]
    prob = point[2]



    if prob > max_prob:
        max_prob = prob
        best_lon = lon
        best_lat  = lat



if max_prob > 0:
    print(f" HIGHEST AURORA PROBABILITY: {max_prob}%")
    print(f"Coordinates: Latitude {best_lat}, Longitude {best_lon}")
else:
    print("Zero aurora probability globally right now. The sun is snoozing.")
