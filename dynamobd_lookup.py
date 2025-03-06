# ~/flink1/udf/dynamodb_lookup.py

from pyflink.table import DataTypes
from pyflink.table.udf import udf
import json
import boto3
from decimal import Decimal

# DynamoDB Lookup Logic
def checkfraud(card_number, amount, zipcode, timestamp):
    """Returns 'FRAUD' or 'LEGIT' after checking DynamoDB."""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('UserTransactionHistory')
    
    response = table.get_item(Key={'card_number': card_number})
    item = response.get('Item')

    if item:
        prev_zip = item.get('last_zipcode')
        prev_time = item['last_transaction_time']
        avg_amount = Decimal(item.get('avg_transaction_amount',0))

        # Ensure `prev_time` and `prev_zip` are not None before using them
        if prev_time is not None and prev_zip is not None:
            if abs(prev_time - timestamp) < 600 and prev_zip != zipcode:
                return 'FRAUD - ZIP Code Mismatch'

        if amount > avg_amount * 8:
            return 'FRAUD - Amount Anomaly'

        # Update only if `prev_time` and `prev_zip` exist
        update_expression = "SET avg_transaction_amount = :a"
        expression_values = {':a': (avg_amount + Decimal(amount)) / 2}

        if timestamp is not None:
            update_expression += ", last_transaction_time = :t"
            expression_values[':t'] = timestamp
        if zipcode is not None:
            update_expression += ", last_zipcode = :z"
            expression_values[':z'] = zipcode


        # Update on Legit Transactions
        table.update_item(
            Key={'card_number': card_number},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
        return 'LEGIT'
    else:
        # Add New User
        table.put_item(
            Item={
                'card_number': card_number,
                'last_zipcode': zipcode if zipcode is not None else "UNKNOWN",
                'last_transaction_time': timestamp if timestamp is not None else 0,
                'avg_transaction_amount': Decimal(amount)
            }
        )
        return 'LEGIT - New User'

# PyFlink UDF Registration for Flink SQL
checkfraud_flink = udf(
    f=checkfraud,
    input_types=[DataTypes.STRING(), DataTypes.DOUBLE(), DataTypes.STRING(), DataTypes.BIGINT()],
    result_type=DataTypes.STRING()
)

#  Export for Flink SQL Usage
__all__ = ['checkfraud','checkfraud_flink']