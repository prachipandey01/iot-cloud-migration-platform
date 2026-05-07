import boto3
import time
import datetime
import json
import random
from decimal import Decimal

REGION = "ap-south-1"
BUCKET = "iot-airquality-data-prachi"
TABLE = "AirQuality_SensorData"

s3 = boto3.client('s3', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE)

ZONES = ["Zone_A_Connaught","Zone_B_Dwarka","Zone_C_Rohini","Zone_D_Noida","Zone_E_Gurugram"]
BATCH_SIZES = [10, 50, 100]

print("=" * 55)
print("   IoT CLOUD THROUGHPUT MONITORING TEST")
print("=" * 55)

results = []

for batch in BATCH_SIZES:
    print(f"\n📊 Testing batch size: {batch} records...")
    
    # S3 throughput test
    s3_start = time.time()
    for i in range(batch):
        zone = random.choice(ZONES)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            "timestamp": timestamp,
            "sensor_id": f"{zone}_S1",
            "zone": zone,
            "pm25_ugm3": round(random.uniform(60, 200), 2),
            "co2_ppm": round(random.uniform(380, 600), 2),
            "temperature_C": round(random.uniform(24, 35), 2)
        }
        s3.put_object(
            Bucket=BUCKET,
            Key=f"throughput-test/{timestamp}_{i}.json",
            Body=json.dumps(payload),
            ContentType='application/json'
        )
    s3_end = time.time()
    s3_time = round(s3_end - s3_start, 2)
    s3_rate = round(batch / s3_time, 2)

    # DynamoDB throughput test
    db_start = time.time()
    for i in range(batch):
        zone = random.choice(ZONES)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        table.put_item(Item={
            "sensor_id": f"{zone}_S1",
            "timestamp": timestamp,
            "zone": zone,
            "pm25_ugm3": Decimal(str(round(random.uniform(60, 200), 2))),
            "co2_ppm": Decimal(str(round(random.uniform(380, 600), 2))),
            "anomaly": random.choice([True, False])
        })
    db_end = time.time()
    db_time = round(db_end - db_start, 2)
    db_rate = round(batch / db_time, 2)

    results.append({
        "batch": batch,
        "s3_time": s3_time,
        "s3_rate": s3_rate,
        "db_time": db_time,
        "db_rate": db_rate
    })

    print(f"  ✅ S3 Upload   : {batch} records in {s3_time}s → {s3_rate} records/sec")
    print(f"  ✅ DynamoDB    : {batch} records in {db_time}s → {db_rate} records/sec")

print("\n" + "=" * 55)
print("   THROUGHPUT SUMMARY")
print("=" * 55)
print(f"{'Batch':<10} {'S3 (rec/s)':<15} {'DynamoDB (rec/s)':<20}")
print("-" * 45)
for r in results:
    print(f"{r['batch']:<10} {r['s3_rate']:<15} {r['db_rate']:<20}")

print("\n✅ Throughput monitoring complete!")