from kafka import KafkaProducer
import pandas as pd
import json
import time

columns = ["card_number","transaction_id","amount","zipcode","timestamp"]
# Load transaction dataset
df = pd.read_csv("/ec2.path/to/csv/file.csv",names=columns, usecols=[0,1,2,3,4])
df_sampled = df.sample(frac=0.001, random_state=42)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v, default =str).encode("utf-8")
)

# Stream transactions to Kafka
for _, row in df_sampled.iterrows():
    transaction = {
        "card_number": str(row["card_number"]),  # Ensure it's a string
        "transaction_id": str(row["transaction_id"]),  # Convert transaction_id to string
        "amount": float(row["amount"]),  # Convert to standard Python float
        "zipcode": str(row["zipcode"]),  # Ensure ZIP code is a string
        "timestamp": int(row["timestamp"])  # Convert timestamp to standard Python int
    }
    producer.send("credit_card_transactions", value=transaction)
    print(f"Sent: {transaction}")
    time.sleep(1)  # Simulate real-time streaming

producer.close()

