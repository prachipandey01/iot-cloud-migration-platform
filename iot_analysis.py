import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("iot_air_quality_data.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['date'] = df['timestamp'].dt.date

print("=== BASIC STATS ===")
print(df[['temperature_C','humidity_pct','co2_ppm','pm25_ugm3','no2_ugm3']].describe())

# --- PLOT 1: Avg PM2.5 by Hour (all zones) ---
hourly_pm25 = df.groupby('hour')['pm25_ugm3'].mean()
plt.figure(figsize=(10,4))
plt.plot(hourly_pm25.index, hourly_pm25.values, marker='o', color='crimson')
plt.title('Average PM2.5 by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('PM2.5 (µg/m³)')
plt.xticks(range(0,24))
plt.grid(True)
plt.tight_layout()
plt.savefig('plot1_pm25_hourly.png')
plt.show()
print("✅ Plot 1 saved")

# --- PLOT 2: Zone-wise Avg CO2 ---
zone_co2 = df.groupby('zone')['co2_ppm'].mean().sort_values(ascending=False)
plt.figure(figsize=(10,4))
sns.barplot(x=zone_co2.index, y=zone_co2.values, palette='Reds_r')
plt.title('Average CO2 Level by Zone')
plt.xlabel('Zone')
plt.ylabel('CO2 (ppm)')
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig('plot2_co2_zone.png')
plt.show()
print("✅ Plot 2 saved")

# --- PLOT 3: Anomaly Detection (PM2.5 > 200) ---
anomalies = df[df['pm25_ugm3'] > 200]
print(f"\n=== ANOMALIES DETECTED: {len(anomalies)} records ===")
print(anomalies[['timestamp','zone','pm25_ugm3','co2_ppm']].head(10))
anomalies.to_csv('anomalies.csv', index=False)
print("✅ Anomalies saved to anomalies.csv")

# --- PLOT 4: Heatmap - Hourly avg PM2.5 per Zone ---
pivot = df.pivot_table(values='pm25_ugm3', index='zone', columns='hour', aggfunc='mean')
plt.figure(figsize=(14,5))
sns.heatmap(pivot, cmap='YlOrRd', linewidths=0.3)
plt.title('PM2.5 Heatmap: Zone vs Hour of Day')
plt.tight_layout()
plt.savefig('plot3_heatmap.png')
plt.show()
print("✅ Plot 3 saved")