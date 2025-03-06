# credit-card-fraud-detection #

# Overview 
This project implements a real-time credit card fraud detection system using Apache Flink, Kafka, DynamoDB, and Iceberg on AWS. Transactions are streamed via Kafka, analyzed in Flink SQL using a Python UDF, and stored in Iceberg for analytics.

# Features 
- Real-time fraud detection based on transaction history.
- Kafka integration for streaming transaction data.
- Flink SQL processing for fraud analysis.
- DynamoDB lookup to track user transaction history.
- Iceberg storage for OLAP queries.
- Kafka alerts for flagged fraudulent transactions.

# Architecture 
- Kafka Producer - Streams transaction data into Kafka.
- Flink SQL Pipeline - Reads transactions, checks DynamoDB, flags fraud, and updates Iceberg.
- DynamoDB - Stores transaction history for fraud checks.
- Kafka Fraud Alerts - Publishes flagged transactions to a separate topic.
- Iceberg - Stores all processed transactions for analytics.

### **Software Requirements**
- **Java** (OpenJDK 11+)
- **Apache Kafka** (3.7.2)
- **Apache Flink** (1.17.2)
- **Python** (3.10+)
- **PyFlink** (1.17.2)
- **Boto3** (AWS SDK for DynamoDB)
- **Cloudpickle** (for Flink UDFs)
- **Apache Iceberg** (Flink Connector)

## Setup Instructions
### **1. Setup Kafka**
```bash
wget https://downloads.apache.org/kafka/3.7.2/kafka_2.13-3.7.2.tgz
tar -xzf kafka_2.13-3.7.2.tgz
cd kafka_2.13-3.7.2
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
```
### **2. Create Kafka Topics**
```bash
bin/kafka-topics.sh --create --topic credit_card_transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
bin/kafka-topics.sh --create --topic fraud_alerts --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
### **3. Setup Apache Flink**
```bash
wget https://archive.apache.org/dist/flink/flink-1.17.2/flink-1.17.2-bin-scala_2.12.tgz
tar -xzf flink-1.17.2-bin-scala_2.12.tgz
cd flink-1.17.2
./bin/start-cluster.sh
```
### **4. Configure Flink SQL Client**
Update `flink-conf.yaml`:
```yaml
rest.address: 0.0.0.0
python.client.executable: /home/ubuntu/flink-env/bin/python3
python.files: /home/ubuntu/flink1/udf/dynamodb_lookup.py
```

### **5. Setup Python Virtual Environment**
```bash
python3 -m venv ~/flink-env
source ~/flink-env/bin/activate
pip install -U pip pyflink boto3 cloudpickle
```

### **6. Start Kafka Producer**
```bash
python3 producer.py
```

### **7. Run Flink SQL Client and Create Tables**
```bash
~/flink1/bin/sql-client.sh -f create_tables.sql
```

### **8. Run Fraud Detection SQL Queries**

## Running the Project
1. Start **Zookeeper** and **Kafka**
2. Start **Flink Cluster**
3. Start **Kafka Producer** to send transactions
4. Execute **Flink SQL Queries** for fraud detection

## Expected Output
- All transactions will be stored in **Iceberg (S3)**.
- Fraudulent transactions will be sent to **fraud_alerts Kafka topic**.

## Contributing
Feel free to fork this repo and contribute! Open an issue or PR for enhancements.
