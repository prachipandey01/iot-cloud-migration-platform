import boto3
import random
import datetime
from decimal import Decimal

REGION = "ap-south-1"
SNS_ARN = "arn:aws:sns:ap-south-1:328113723976:AirQuality-Alerts"
TABLE = "AirQuality_SensorData"

sns = boto3.client('sns', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE)

ZONES = [
    "Zone_A_Connaught",
    "Zone_B_Dwarka", 
    "Zone_C_Rohini",
    "Zone_D_Noida",
    "Zone_E_Gurugram"
]

print("🔍 Processing sensor readings and checking for anomalies...\n")

alerts_sent = 0

for zone in ZONES:
    for sensor_num in [1, 2]:
        sensor_id = f"{zone}_S{sensor_num}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pm25 = round(random.uniform(60, 250), 2)
        co2 = round(random.uniform(380, 520), 2)
        temp = round(random.uniform(24, 35), 2)
        anomaly = pm25 > 150

        # Write to DynamoDB
        table.put_item(Item={
            "sensor_id": sensor_id,
            "timestamp": timestamp,
            "zone": zone,
            "temperature_C": Decimal(str(temp)),
            "co2_ppm": Decimal(str(co2)),
            "pm25_ugm3": Decimal(str(pm25)),
            "anomaly": anomaly
        })

        if anomaly:
            # Send SNS alert
            message = f"""
🚨 AIR QUALITY ALERT — ANOMALY DETECTED

Sensor ID  : {sensor_id}
Zone       : {zone}
Timestamp  : {timestamp}
PM2.5      : {pm25} µg/m³ (SEVERE — Limit: 150)
CO2        : {co2} ppm
Temperature: {temp}°C

Action Required: Immediate inspection recommended.
"""
            sns.publish(
                TopicArn=SNS_ARN,
                Subject=f"🚨 PM2.5 Alert — {zone}",
                Message=message
            )
            alerts_sent += 1
            print(f"🚨 ALERT SENT | {sensor_id} | PM2.5: {pm25} µg/m³")
        else:
            print(f"✅ Normal    | {sensor_id} | PM2.5: {pm25} µg/m³")

print(f"\n🎉 Done! {alerts_sent} alert(s) sent to dev.prachipandey@gmail.com")