import json
import boto3


def lambda_handler(event, context):
    # DynamoDB Stream 이벤트 처리
    if "Records" in event:
        for record in event["Records"]:
            if record["eventName"] == "INSERT":
                handle_insert(record)
            elif record["eventName"] == "MODIFY":
                handle_modify(record)
            elif record["eventName"] == "REMOVE":
                handle_remove(record)

    return {
        "statusCode": 200,
        "body": json.dumps("Successfully processed DynamoDB stream event"),
    }


def handle_insert(record):
    new_image = record["dynamodb"]["NewImage"]
    print(f"New item inserted: {json.dumps(new_image)}")
    # 여기에 삽입 이벤트 처리 로직 추가


def handle_modify(record):
    old_image = record["dynamodb"]["OldImage"]
    new_image = record["dynamodb"]["NewImage"]
    print(f"Item modified - Old: {json.dumps(old_image)}, New: {json.dumps(new_image)}")
    # 여기에 수정 이벤트 처리 로직 추가


def handle_remove(record):
    old_image = record["dynamodb"]["OldImage"]
    print(f"Item removed: {json.dumps(old_image)}")
    # 여기에 삭제 이벤트 처리 로직 추가
