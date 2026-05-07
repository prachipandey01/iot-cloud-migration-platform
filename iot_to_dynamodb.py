import boto3
import json
import random
import datetime
from decimal import Decimal

# --- CONFIG ---
REGION = "ap-south-1"
TABLE = "AirQuality_SensorData"

dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE)

ZONES = [
    "Zone_A_Connaught",
    "Zone_B_Dwarka",
    "Zone_C_Rohini",
    "Zone_D_Noida",
    "Zone_E_Gurugram"
]

print("Starting DynamoDB ingestion...\n")

count = 0
for zone in ZONES:
    for sensor_num in [1, 2]:
        sensor_id = f"{zone}_S{sensor_num}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pm25 = round(random.uniform(60, 180), 2)
        anomaly = pm25 > 150

        item = {
            "sensor_id": sensor_id,
            "timestamp": timestamp,
            "zone": zone,
            "temperature_C": Decimal(str(round(random.uniform(24, 35), 2))),
            "humidity_pct": Decimal(str(round(random.uniform(45, 75), 2))),
            "co2_ppm": Decimal(str(round(random.uniform(380, 520), 2))),
            "pm25_ugm3": Decimal(str(pm25)),
            "no2_ugm3": Decimal(str(round(random.uniform(25, 60), 2))),
            "anomaly": anomaly
        }

        table.put_item(Item=item)
        count += 1
        flag = "🚨 ANOMALY" if anomaly else "✅ Normal"
        print(f"{flag} | {sensor_id} | PM2.5: {pm25} µg/m³")

print(f"\n🎉 {count} records written to DynamoDB successfully!")