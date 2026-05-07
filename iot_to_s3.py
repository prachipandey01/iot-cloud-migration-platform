import boto3
import json
import random
import datetime
import time

# --- CONFIG ---
BUCKET = "iot-airquality-data-prachi"
REGION = "ap-south-1"

s3 = boto3.client('s3', region_name=REGION)

print("Starting IoT data ingestion to S3...\n")

for i in range(5):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    filename = f"sensor-data/zone-a-connaught/{now.strftime('%Y%m%d_%H%M%S')}_reading.json"

    payload = {
        "timestamp": timestamp,
        "sensor_id": "Zone-A-Connaught-S1",
        "zone": "Zone_A_Connaught",
        "temperature_C": round(random.uniform(24, 35), 2),
        "humidity_pct": round(random.uniform(45, 75), 2),
        "co2_ppm": round(random.uniform(380, 520), 2),
        "pm25_ugm3": round(random.uniform(60, 150), 2),
        "no2_ugm3": round(random.uniform(25, 60), 2)
    }

    s3.put_object(
        Bucket=BUCKET,
        Key=filename,
        Body=json.dumps(payload),
        ContentType='application/json'
    )

    print(f"✅ Reading {i+1} uploaded to S3:")
    print(f"   File: {filename}")
    print(f"   PM2.5: {payload['pm25_ugm3']} | CO2: {payload['co2_ppm']} | Temp: {payload['temperature_C']}°C\n")
    time.sleep(1)

print("🎉 All 5 readings successfully ingested to AWS S3!")