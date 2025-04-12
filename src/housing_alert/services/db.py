"""DynamoDB 래퍼 – 사용자·공고 CRUD + 테이블 자동 생성."""

import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional

from housing_alert.config import settings

dynamodb = boto3.resource("dynamodb", region_name=settings.aws_region)
client = dynamodb.meta.client

# ---------- 테이블 보장 ----------


def _ensure_table(table_name: str, key_name: str):
    try:
        client.describe_table(TableName=table_name)
    except client.exceptions.ResourceNotFoundException:
        client.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": key_name, "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": key_name, "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        dynamodb.Table(table_name).wait_until_exists()


_ensure_table(settings.USER_TABLE, "user_id")
_ensure_table(settings.NOTICE_TABLE, "notice_id")

user_table = dynamodb.Table(settings.USER_TABLE)
notice_table = dynamodb.Table(settings.NOTICE_TABLE)

# ---------- User ----------


def save_user(user: Dict[str, Any]) -> None:
    user_table.put_item(Item=user)


def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    try:
        resp = user_table.get_item(Key={"user_id": user_id})
        return resp.get("Item")
    except ClientError as e:
        print("DynamoDB get_user error", e)
        return None


# ---------- Notice ----------


def get_notice(notice_id: str) -> Optional[Dict[str, Any]]:
    try:
        resp = notice_table.get_item(Key={"notice_id": notice_id})
        return resp.get("Item")
    except ClientError as e:
        print("DynamoDB get_notice error", e)
        return None
