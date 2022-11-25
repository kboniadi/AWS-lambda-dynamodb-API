import os
import pathlib

import boto3
from boto3.resources.base import ServiceResource
from mypy_boto3_dynamodb import DynamoDBServiceResource


def initialize_db() -> DynamoDBServiceResource:
    # ddb = boto3.resource('dynamodb',
    #                      region_name=Config.DB_REGION_NAME,
    #                      aws_access_key_id=Config.DB_ACCESS_KEY_ID,
    #                      aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY)

    ddb = boto3.resource('dynamodb',
                         endpoint_url='http://db:8000',
                         region_name='example',
                         aws_access_key_id='example',
                         aws_secret_access_key='example')
    return ddb