-- 1. Run Fraud Detection and Store All Transactions in Iceberg
INSERT INTO iceberg_transactions
SELECT 
    CAST(card_number AS STRING),
    CAST(transaction_id AS STRING),
    CAST(amount AS DOUBLE),
    CAST(zipcode AS STRING),
    CAST(`timestamp` AS BIGINT),
    checkfraud_flink(
        CAST(card_number AS STRING), 
        CAST(amount AS DOUBLE), 
        CAST(zipcode AS STRING), 
        CAST(`timestamp` AS BIGINT)
    ) AS decision
FROM credit_card_transactions;

-- 2. Send Only Fraud Alerts to a Kafka Topic
INSERT INTO fraud_alerts
SELECT 
    CAST(card_number AS STRING),
    CAST(transaction_id AS STRING),
    CAST(amount AS DOUBLE),
    CAST(zipcode AS STRING),
    CAST(`timestamp` AS BIGINT),
    checkfraud_flink(
        CAST(card_number AS STRING), 
        CAST(amount AS DOUBLE), 
        CAST(zipcode AS STRING), 
        CAST(`timestamp` AS BIGINT)
    ) AS alert
FROM credit_card_transactions
WHERE TRIM(checkfraud_flink(
        CAST(card_number AS STRING), 
        CAST(amount AS DOUBLE), 
        CAST(zipcode AS STRING), 
        CAST(`timestamp` AS BIGINT)
    )) LIKE 'FRAUD%';
