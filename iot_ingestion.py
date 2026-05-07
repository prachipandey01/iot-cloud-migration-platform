import time
import json
import random
import datetime
from awsiot import mqtt_connection_builder

# --- CONFIG ---
ENDPOINT = "a2exzp34bh60mv-ats.iot.ap-south-1.amazonaws.com"
CLIENT_ID = "Zone-A-Connaught-S1"
CERT     = "9a7239cd62de2581b26e0dc33e536c91b402b8192bce22ea7d432d58d0b10c19-certificate.pem.crt"
KEY      = "9a7239cd62de2581b26e0dc33e536c91b402b8192bce22ea7d432d58d0b10c19-private.pem.key"
CA       = "AmazonRootCA1.pem"
TOPIC    = "airquality/zone-a/sensor1"
MESSAGES = 5  # number of readings to send

# --- BUILD CONNECTION ---
print("Connecting to AWS IoT Core...")
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=CERT,
    pri_key_filepath=KEY,
    ca_filepath=CA,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

connect_future = mqtt_connection.connect()
connect_future.result()
print("✅ Connected to AWS IoT Core!\n")

# --- PUBLISH SENSOR DATA ---
for i in range(MESSAGES):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "timestamp": now,
        "sensor_id": CLIENT_ID,
        "zone": "Zone_A_Connaught",
        "temperature_C": round(random.uniform(24, 35), 2),
        "humidity_pct": round(random.uniform(45, 75), 2),
        "co2_ppm": round(random.uniform(380, 520), 2),
        "pm25_ugm3": round(random.uniform(60, 150), 2),
        "no2_ugm3": round(random.uniform(25, 60), 2)
    }
    
    mqtt_connection.publish(
        topic=TOPIC,
        payload=json.dumps(payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE if False else 1
    )
    
    print(f"📡 Message {i+1} sent:")
    print(f"   PM2.5: {payload['pm25_ugm3']} µg/m³ | CO2: {payload['co2_ppm']} ppm | Temp: {payload['temperature_C']}°C")
    time.sleep(2)

# --- DISCONNECT ---
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("\n✅ Disconnected. Ingestion complete!")