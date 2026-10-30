import boto3
from botocore.exceptions import ClientError
from app.config import settings

dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
table = dynamodb.Table(settings.DYNAMODB_TABLE)

def save_url(short_code: str, original_url: str, created_at: str):
    try:
        table.put_item(
            Item={
                "short_code": short_code,
                "original_url": original_url,
                "created_at": created_at,
            }
        )
    except ClientError as e:
        raise RuntimeError(f"Error al typear en DynamoDB: {e.response['Error']['Message']}")

def get_url_item(short_code: str):
    try:
        response = table.get_item(Key={"short_code": short_code})
        return response.get("Item")
    except ClientError as e:
        raise RuntimeError(f"Consulta erronea DynamoDB: {e.response['Error']['Message']}")