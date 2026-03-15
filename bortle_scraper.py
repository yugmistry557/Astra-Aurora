import requests
import re

def get_bortle_class(lat, lon):
    print(f"Scraping dark sky data for Lat: {lat}, Lon: {lon}...")
    
    # Clear Outside dynamically generates forecast pages for any coordinate
    url = f"https://clearoutside.com/forecast/{lat}/{lon}"
    
    # We have to pretend to be a normal web browser, or their security will block our code
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        html_content = response.text
        
        # Pure hacker regex: We scan the giant wall of HTML text looking for 
        # the phrase "Bortle Class: " and grab the digits right after it.
        # \d+ means "one or more numbers"
        match = re.search(r'Bortle.*?(\d+)', html_content, re.IGNORECASE)
        
        if match:
            bortle = int(match.group(1))
            print(f"Success! Found Bortle Class {bortle}")
            return bortle
        else:
            print("Couldn't find the Bortle class. Defaulting to 5.")
            return 5
            
    except Exception as e:
        print(f"Scraper failed: {e}. Defaulting to 5.")
        return 5

# Test it out! Let's try London (Lat: 51.50, Lon: -0.12)
if __name__ == "__main__":
    bortle = get_bortle_class(51.50, -0.12)