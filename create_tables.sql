CREATE TABLE credit_card_transactions (
    card_number STRING,
    transaction_id STRING,
    amount DOUBLE,
    zipcode STRING,
    `timestamp` BIGINT
) WITH (
    'connector' = 'kafka',
    'topic' = 'credit_card_transactions',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'fraud-check-group',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
);

-- 2. Kafka Sink Table (fraud alerts)
CREATE TABLE fraud_alerts (
    card_number STRING,
    transaction_id STRING,
    amount DOUBLE,
    zipcode STRING,
    timestamp_ts BIGINT,
    alert STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'fraud_alerts',
    'properties.bootstrap.servers' = 'localhost:9092',
    'properties.group.id' = 'fraud-alert-group', 
    'scan.startup.mode' = 'earliest-offset', 
    'format' = 'json'
);

-- 3. Iceberg Sink Table (for all transactions)
CREATE TABLE iceberg_transactions (
    card_number STRING,
    transaction_id STRING,
    amount DOUBLE,
    zipcode STRING,
    timestamp_ts BIGINT,
    decision STRING
) WITH (
    'connector' = 'iceberg',
    'catalog-name' = 'my_iceberg_catalog',
    'warehouse' = 's3a://fraud-detection-iceberg/',
    'format' = 'parquet'
);
