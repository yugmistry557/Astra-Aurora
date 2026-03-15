import ephem 
import math
from datetime import datetime

def calculate_visibility_score(probability, cloud_cover, bortle_class, lat, lon):
    
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = datetime.utcnow()
    
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)
    
    # Convert altitude from radians to degrees for easier math
    sun_alt = math.degrees(sun.alt)
    moon_alt = math.degrees(moon.alt)
    
    # ephem gives moon phase as a percentage (0.0 to 100.0)
    moon_illumination = moon.phase / 100.0 
    
    # ---------------------------------------------------------
    # 2. THE TERMINATOR CHECK (Is it actually dark?)
    # ---------------------------------------------------------
    # If the sun is higher than -6 degrees, it's daytime or bright twilight. 
    # The aurora is completely invisible. Hard zero.
    if sun_alt > -6.0:
        return 0.0
        
    # ---------------------------------------------------------
    # 3. CALCULATE THE MULTIPLIERS
    # ---------------------------------------------------------
    
    # Cloud Penalty: 0% clouds = 1.0 multiplier, 100% clouds = 0.0 multiplier
    cloud_factor = 1.0 - (cloud_cover / 100.0)
    
    # Base Darkness (Bortle 1 = 1.0, Bortle 9 = ~0.11)
    base_darkness = (10 - bortle_class) / 9.0
    
    # Lunar Penalty: If the moon is up, it acts like light pollution
    moon_penalty = 0.0
    if moon_alt > 0:
        # A full moon (1.0) reduces the darkness score by up to 40%
        moon_penalty = moon_illumination * 0.40 
        
    # Combine Bortle and Moon into final darkness factor (preventing negative numbers)
    final_darkness_factor = max(0.1, base_darkness - moon_penalty)
    
    # ---------------------------------------------------------
    # 4. THE FINAL MASTER SCORE
    # ---------------------------------------------------------
    raw_score = probability * cloud_factor * final_darkness_factor
    
    return round(raw_score, 2)


# --- Let's test it with a real-world scenario! ---
if __name__ == "__main__":
    # Test coordinates: Reykjavik, Iceland
    test_lat = 64.14
    test_lon = -21.92
    
    score = calculate_visibility_score(
        probability=85, 
        cloud_cover=10, 
        bortle_class=3, 
        lat=test_lat, 
        lon=test_lon
    )
    
    print(f"Testing Iceland coordinates (Lat: {test_lat}, Lon: {test_lon}) right now...")
    print(f"Master Visibility Score: {score} / 100")