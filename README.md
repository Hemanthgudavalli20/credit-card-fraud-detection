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

