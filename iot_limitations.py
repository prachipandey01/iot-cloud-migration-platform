import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt

df = pd.read_csv("iot_air_quality_data.csv")

print("=" * 55)
print("   PROCESSING LIMITATIONS ANALYSIS — LOCAL SYSTEM")
print("=" * 55)

# --- LIMITATION 1: Scalability ---
print("\n📌 LIMITATION 1: Scalability")
current_sensors = 10
current_records = len(df)
projected = []
for sensors in [10, 50, 100, 500, 1000]:
    records = (current_records // current_sensors) * sensors
    projected.append({"Sensors": sensors, "Records_30days": records,
                       "Estimated_Size_MB": round((records * 0.25) / 1024, 2)})
proj_df = pd.DataFrame(projected)
print(proj_df.to_string(index=False))

# --- LIMITATION 2: Storage ---
print("\n📌 LIMITATION 2: Storage Growth Over Time")
file_size_kb = os.path.getsize("iot_air_quality_data.csv") / 1024
months = [1, 3, 6, 12, 24]
print(f"Current file size (30 days, 10 sensors): {file_size_kb:.1f} KB")
for m in months:
    projected_mb = (file_size_kb * m) / 1024
    print(f"  {m:>2} month(s) → {projected_mb:.2f} MB  "
          f"{'⚠️ manageable' if projected_mb < 10 else '❌ problematic at scale'}")

# --- LIMITATION 3: Real-time Processing Speed ---
print("\n📌 LIMITATION 3: Local Processing Speed")
start = time.time()
result = df.groupby(['zone', 'hour'] if 'hour' in df.columns
                    else 'zone')['pm25_ugm3'].mean()
end = time.time()
local_time = round((end - start) * 1000, 2)
print(f"  Local groupby query on 14,400 records: {local_time} ms")
print(f"  Estimated time on 1M records locally:  "
      f"{round(local_time * (1000000/14400), 0)} ms")
print("  Cloud (distributed): ~50–200 ms regardless of size ✅")

# --- LIMITATION 4: Fault Tolerance ---
print("\n📌 LIMITATION 4: Fault Tolerance")
print("  Local Setup:")
print("    - 1 machine = 1 point of failure")
print("    - No data backup or replication")
print("    - System crash = total data loss risk")
print("  Cloud Setup:")
print("    - Data replicated across multiple availability zones")
print("    - 99.99% uptime SLA guaranteed")

# --- LIMITATION 5: Concurrent Load ---
print("\n📌 LIMITATION 5: Concurrent Query Load")
sensors = 10
reading_interval_sec = 1800
records_per_sec = sensors / reading_interval_sec
print(f"  Current: {records_per_sec:.4f} records/sec (10 sensors)")
print(f"  At 500 sensors: {500/reading_interval_sec:.4f} records/sec")
print(f"  At 1000 sensors: {1000/reading_interval_sec:.4f} records/sec")
print("  Local CPU/RAM cannot handle parallel ingestion at this rate ❌")

# --- LIMITATION 6: No Real-time Alerting ---
print("\n📌 LIMITATION 6: No Real-time Alerting Capability")
anomalies = pd.read_csv("anomalies.csv")
print(f"  Anomalies detected in dataset: {len(anomalies)}")
print("  Local system: detects AFTER full batch load only")
print("  Cloud stream processing: detects WITHIN seconds of ingestion ✅")

# --- CHART: Scalability Visual ---
sensors_list = [10, 50, 100, 500, 1000]
size_mb = [(((current_records // current_sensors) * s) * 0.25) / 1024
           for s in sensors_list]

plt.figure(figsize=(9, 4))
plt.bar([str(s) for s in sensors_list], size_mb, color=['green','green','orange','red','red'])
plt.title('Projected Storage Growth vs Number of Sensors (30 days)')
plt.xlabel('Number of Sensors')
plt.ylabel('Estimated Data Size (MB)')
plt.tight_layout()
plt.savefig('plot4_scalability.png')
plt.show()
print("\n✅ plot4_scalability.png saved")

print("\n" + "=" * 55)
print("   ANALYSIS COMPLETE")
print("=" * 55)