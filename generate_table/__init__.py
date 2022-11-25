import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource

def initialize_db() -> DynamoDBServiceResource:
    ddb = boto3.resource('dynamodb',
                         endpoint_url='http://localhost:8000',
                         region_name='example',
                         aws_access_key_id='example',
                         aws_secret_access_key='example')

    return ddb