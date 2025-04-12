import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        logger.info(f"New file uploaded: s3://{bucket}/{key}")

        # Put the file name as the ID in DynamoDB
        response = table.put_item(
            Item={
                'id': key
            }
        )

        logger.info(f"Inserted item into DynamoDB with id: {key}")
