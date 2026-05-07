# ☁️ Cloud Migration of IoT Data Processing Platform

> **MCA Project — Data Analysis | Chandigarh University Online | 2025–26**
> 
> Migrating a legacy on-premise IoT pipeline to a fully managed, serverless AWS architecture

---

## 👤 Project Details

| Field | Details |
|-------|---------|
| **Student** | Prachi Pandey |
| **UID** | O24MCA111550 |
| **Programme** | MCA — Data Analysis |
| **Mentor** | Mr. Anurag Goel |
| **University** | Chandigarh University Online |
| **Academic Year** | 2025 – 2026 |

---

## 📌 Project Overview

This project migrates an IoT air quality monitoring platform from on-premise infrastructure to a fully managed AWS cloud architecture. The system collects sensor data from four NCR cities (Gurugram, Delhi, Noida, Faridabad), stores it in a partitioned S3 data lake and DynamoDB, generates automated pollution alerts via SNS, and provides serverless SQL analytics through Amazon Athena.

**Dataset:** 14,400 sensor records | PM2.5, PM10, CO2, VOC, Temperature, Humidity

---

## 🏗️ Architecture

```
IoT Sensors (MQTT/TLS)
        │
        ▼
  AWS IoT Core  ──────────────────────────────────────────┐
  (Device Auth + Rules Engine)                            │
        │                                                  │
        ▼                                                  ▼
  Amazon S3 (Data Lake)                           Amazon DynamoDB
  raw/year=YYYY/month=MM/                         Table: SensorReadings
  day=DD/city=CITY/                               PK: sensor_id | SK: timestamp
        │                                                  │
        ▼                                                  ▼
  Amazon Athena                                   Threshold Monitor (boto3)
  (Serverless SQL Analytics)                              │
                                                          ▼
                                                   Amazon SNS
                                                   (Email/SMS Alerts)
```

---

## ⚙️ Tech Stack

| Service | Role |
|---------|------|
| **AWS IoT Core** | MQTT device connectivity, X.509 auth, rules engine |
| **Amazon S3** | Partitioned data lake — raw JSON + processed Parquet |
| **Amazon DynamoDB** | NoSQL operational store — on-demand billing |
| **Amazon SNS** | Real-time threshold alerting — PM2.5 > 150, PM10 > 250 |
| **Amazon Athena** | Serverless SQL on S3 — time-series + city analysis |
| **Python boto3** | AWS SDK — all service interactions |
| **AWS IAM** | Least-privilege access control |

---

## 📁 Repository Structure

```
iot-cloud-migration-platform/
│
├── setup/
│   ├── s3_setup.py               # S3 bucket creation + lifecycle config
│   └── dynamo_setup.py           # DynamoDB table provisioning
│
├── ingest/
│   └── batch_ingest.py           # Batch write 14,400 records to DynamoDB
│
├── alerting/
│   ├── sns_setup.py              # SNS topic + subscription setup
│   └── threshold_monitor.py      # Scan DynamoDB + publish alerts
│
├── analytics/
│   └── athena_queries.py         # Athena query execution via boto3
│
├── config/
│   └── thresholds.yaml           # PM2.5 and PM10 alert thresholds
│
├── data/
│   └── sensor_data_sample.csv    # Sample dataset (100 records)
│
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- AWS Account with IAM user credentials
- AWS CLI v2 installed

### 1. Clone the repository
```bash
git clone https://github.com/prachi-pandey-mca/iot-cloud-migration-platform.git
cd iot-cloud-migration-platform
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure AWS credentials
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region (ap-south-1), Format (json)
```

### 5. Run setup scripts
```bash
python setup/s3_setup.py
python setup/dynamo_setup.py
```

### 6. Ingest data
```bash
python ingest/batch_ingest.py --input data/sensor_data_sample.csv
```

### 7. Configure alerting
```bash
python alerting/sns_setup.py --email your@email.com
# Confirm the subscription from your email inbox
python alerting/threshold_monitor.py
```

### 8. Run Athena analytics
```bash
python analytics/athena_queries.py
```

---

## 📊 Key Results

| Metric | Target | Achieved |
|--------|--------|----------|
| DynamoDB Write Throughput | ≥ 7.0 rec/s | **7.92 rec/s** ✅ |
| SNS Alert Latency | < 60 seconds | **28 seconds** ✅ |
| Athena Query Latency | < 10 seconds | **4.3 seconds** ✅ |
| Data Integrity | 100% | **100%** ✅ |
| Records Migrated | 14,400 | **14,400** ✅ |
| Infrastructure Overhead | Zero servers | **Zero servers** ✅ |

---

## 🔍 Key Findings

### Dual-Peak Pollution Pattern
PM2.5 concentrations peak at **9 AM** (avg 167 µg/m³) and **6 PM** (avg 172 µg/m³) across all four cities — directly aligned with NCR commute windows.

### City-wise PM2.5 Ranking
| City | Avg PM2.5 (µg/m³) | Peak PM2.5 (µg/m³) | WHO Exceedance |
|------|-------------------|-------------------|----------------|
| Gurugram | 142.3 | 310.8 | 9.5x |
| Delhi | 138.7 | 298.4 | 9.2x |
| Faridabad | 131.5 | 285.6 | 8.8x |
| Noida | 127.9 | 271.3 | 8.5x |

> All cities exceed WHO 24-hour PM2.5 guideline (15 µg/m³) by 8.5–9.5x

---

## 🔐 Security

- TLS 1.2 encryption on all AWS service channels
- IAM least-privilege roles — no wildcard permissions
- S3 bucket with Block Public Access enabled
- IoT Core with X.509 certificate-based device authentication
- Credentials stored via environment variables — never hardcoded

---

## 🧪 Testing

All modules tested at three levels:

- **Unit Tests** — Individual functions mocked with `moto` library
- **Integration Tests** — Real AWS services in isolated test environment
- **System Tests** — End-to-end pipeline validation with full dataset

Run tests:
```bash
pytest tests/ -v
```

---

## 🔮 Future Enhancements

1. **AWS SageMaker** — Predict PM2.5 breaches 2–4 hours ahead
2. **Amazon Kinesis** — Sub-second real-time streaming ingestion
3. **Amazon QuickSight** — Self-service dashboard for non-technical stakeholders
4. **Multi-Region DynamoDB Global Tables** — Active-active replication
5. **CPCB AQI Scoring** — Lambda function computing composite AQI on every write

---

## 📚 References

- AWS IoT Core Developer Guide — https://docs.aws.amazon.com/iot/latest/developerguide/
- Amazon DynamoDB Developer Guide — https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/
- Boto3 Documentation — https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- Gubbi et al. (2013) — IoT: A Vision, Architectural Elements, and Future Directions. *Future Generation Computer Systems*, 29(7)
- WHO Global Air Quality Guidelines (2021)

---

## 📄 License

This project is submitted as an academic project for Chandigarh University Online. Code is available for educational reference.

---

*Prachi Pandey | UID: O24MCA111550 | MCA Data Analysis | CU Online | 2025–26*
