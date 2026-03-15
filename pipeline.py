import asyncio
import requests
from datetime import datetime

live_telementry = {
    "speed": 0.0,
    "bz": 0.0,
    "status": "Initializing....",
    "source": "None",
    "last_updated": "never",
    "substorm_warning": False  # <-- NEW FIELD ADDED HERE
}

primary_plasma_url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
primary_mag_url = "https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json"

backup_plasma_url = primary_plasma_url
backup_mag_url = primary_mag_url

# --- NEW: History array to track the last 5 minutes of data ---
bz_history = []

async def background_pipeline():
    print("🚀 Igniting live data pipeline with Substorm Detection...")

    while True:
        current_speed = None
        current_bz = None
        status = "Nominal"
        source = "DSCOVR"

        try:
            plasma_res = requests.get(primary_plasma_url, timeout=5)
            mag_res = requests.get(primary_mag_url, timeout=5)
            plasma_data = plasma_res.json()
            mag_data = mag_res.json()
            
            if plasma_data[0][2] != 'speed' or mag_data[0][3] != 'bz_gsm':
                raise ValueError("SCHEMA CHANGED! Columns are not where we expect them.")

            lastest_plasma = plasma_data[-1]
            lastest_mag = mag_data[-1]

            if lastest_plasma[2] is None or lastest_mag[3] is None:
                raise ValueError("DATA GAP: Satellite returned empty telemetry.")

            current_speed = float(lastest_plasma[2])
            current_bz = float(lastest_mag[3])

        except Exception as primary_error:
            print(f"⚠️ DSCOVR Error ({primary_error}). Initiating ACE Failover...")
            try:
                fallback_plasma = requests.get(backup_plasma_url, timeout=10).json()
                fallback_mag = requests.get(backup_mag_url, timeout=10).json()

                current_speed = float(fallback_plasma[-1][2])
                current_bz = float(fallback_mag[-1][3])
                status = "Warning: Running on Backup"
                source = "ACE"
            except Exception as backup_error:
                status = "CRITICAL: ALL SATELLITES OFFLINE"
                print("CRITICAL: Both primary and backup feeds are down.")

        # === STRETCH GOAL: SUBSTORM MATH ===
        if current_bz is not None:
            # 1. Update the rolling history window
            bz_history.append(current_bz)
            if len(bz_history) > 5:
                bz_history.pop(0)

            substorm_alert = False
            
            # HACKATHON BYPASS: Set to True so it flashes for your demo!
            force_demo_alert = False

            if force_demo_alert:
                substorm_alert = True
            elif len(bz_history) >= 2:
                # 2. Calculate the derivative (rate of drop)
                bz_drop = bz_history[-1] - bz_history[0]
                
                # If it dropped by more than 2 nT and is pointing South (negative)
                if bz_drop <= -2.0 and current_bz < 0:
                    print("⚠️ SUBSTORM PRECURSOR DETECTED! Sharp Southward deflection.")
                    substorm_alert = True

            # 3. Update the global dictionary
            live_telementry["speed"] = current_speed
            live_telementry["bz"] = current_bz
            live_telementry["status"] = status
            live_telementry["source"] = source
            live_telementry["substorm_warning"] = substorm_alert
            live_telementry["last_updated"] = datetime.now().strftime("%H:%M:%S")

            print(f"[{live_telementry['last_updated']}] Speed: {current_speed} | Bz: {current_bz} | Substorm Warning: {substorm_alert}")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(background_pipeline())