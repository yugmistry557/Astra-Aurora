import requests

plasma_url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
mag_url = "https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json"
plasma_data = requests.get(plasma_url).json()
mag_data = requests.get(mag_url).json()

latest_plasma = plasma_data[-1]
latest_mag = mag_data[-1]

try: 
    speed = float(latest_plasma[2])
    bz = float(latest_mag[3])
    print(f"Timestamp: {latest_plasma[0]}")
    print(f"Solar Wind Speed: {speed} km/s")
    print(f"Magnetic Field (Bz): {bz} nT")
   
    if speed > 500 and bz < -7:
        print("PRIME AURORA CONDITIONS! Both thresholds met. Substorm likely.")
    elif speed > 500:
        print("Wind is fast enough, but Bz is not pointing south. No aurora.")
    elif bz < -7:
        print("Bz is southward, but solar wind is too slow to punch through.")
    else:
        print("Space weather is quiet. Get some sleep.")

except TypeError:
    print("NOAA dropped a data packet for this minute. Run the script again!")