import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- CONFIG ---
ZONES = ["Zone_A_Connaught", "Zone_B_Dwarka", "Zone_C_Rohini", 
         "Zone_D_Noida", "Zone_E_Gurugram"]
SENSORS_PER_ZONE = 2
DAYS = 30  # 1 month of data
INTERVAL_MINUTES = 30  # reading every 30 mins

random.seed(42)
np.random.seed(42)

# --- DATA GENERATION ---
records = []
start_time = datetime(2024, 3, 1, 0, 0, 0)
total_intervals = (DAYS * 24 * 60) // INTERVAL_MINUTES

for zone in ZONES:
    for sensor_num in range(1, SENSORS_PER_ZONE + 1):
        sensor_id = f"{zone}_S{sensor_num}"
        
        for i in range(total_intervals):
            timestamp = start_time + timedelta(minutes=i * INTERVAL_MINUTES)
            hour = timestamp.hour

            # Realistic hourly patterns
            traffic_factor = 1.5 if 8 <= hour <= 10 or 17 <= hour <= 20 else 1.0
            night_factor = 0.6 if 0 <= hour <= 5 else 1.0

            record = {
                "timestamp": timestamp,
                "sensor_id": sensor_id,
                "zone": zone,
                "temperature_C": round(np.random.normal(28, 4) * night_factor, 2),
                "humidity_pct": round(np.random.normal(60, 10), 2),
                "co2_ppm": round(np.random.normal(400, 50) * traffic_factor, 2),
                "pm25_ugm3": round(np.random.normal(85, 20) * traffic_factor, 2),
                "no2_ugm3": round(np.random.normal(40, 10) * traffic_factor, 2),
            }

            # Inject anomalies (~2% of data)
            if random.random() < 0.02:
                record["pm25_ugm3"] = round(random.uniform(200, 350), 2)
                record["co2_ppm"] = round(random.uniform(700, 900), 2)

            records.append(record)

# --- SAVE ---
df = pd.DataFrame(records)
df.to_csv("iot_air_quality_data.csv", index=False)
print(f"✅ Data generated: {len(df)} records")
print(df.head())