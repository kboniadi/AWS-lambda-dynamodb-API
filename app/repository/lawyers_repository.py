import logging
from flask import jsonify
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb import DynamoDBServiceResource

class LawyersRepository:
    def __init__(self, db: DynamoDBServiceResource) -> None:
        self.__db = db

    def get_all(self):
        try:
            table = self.__db.Table('Core')
            response = table.query(
                KeyConditionExpression=Key('category').eq("lawyer")
            )
        except ClientError as e:
            logging.error(
                "Couldn't get all lawyers. Here's why: %s: %s",
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise
        else:
            return response.get('Items', None)

    def get_lawyer(self, email: str):
        try:
            table = self.__db.Table('Core')
            response = table.get_item(Key={'category': "lawyer", 'email': email})
        except ClientError as e:
            logging.error(
                "Couldn't get lawyer %s. Here's why: %s: %s", email,
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise
        else:
            return response.get('Item', None)

    def create_lawyer(self, lawyer: dict) -> None:
        try:
            lawyer['category'] = "lawyer"
            table = self.__db.Table('Core')
            _ = table.put_item(Item=lawyer, )
        except ClientError as e:
            logging.error(
                "Couldn't create %s's account. Here's why: %s: %s", lawyer["name"],
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise

    def update_lawyer(self, lawyer: dict) -> None:
        try:
            table = self.__db.Table('Core')
            _ = table.update_item(
            Key={'category': "lawyer", 'email': lawyer.get('email')},
            UpdateExpression="""
                set
                    #title=:title,
                    #name=:name,
                    #languages=:languages,
                    #location=:location,
                    #phone=:phone,
                    #description=:description,
                    #expertise=:expertise
            """,
            ExpressionAttributeValues={
                ':title': lawyer.get('title'),
                ':name': lawyer.get('name'),
                ':languages': lawyer.get('languages'),
                ':location': lawyer.get('location'),
                ':phone': lawyer.get('phone'),
                ':description': lawyer.get('description'),
                ':expertise': lawyer.get('expertise')
            },
            ExpressionAttributeNames={
                "#title": "title",
                "#name": "name",
                "#languages": "languages",
                "#location": "location",
                "#phone": "phone",
                "#description": "description",
                "#expertise": "expertise",
            },
            ReturnValues="UPDATED_NEW"
        )
        except ClientError as e:
            logging.error(
                "Couldn't update %s's account info. Here's why: %s: %s", lawyer["name"],
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise

    def delete_lawyer(self, email: str) -> None:
        try:
            table = self.__db.Table('Core')
            _ = table.delete_item(
                Key={'category': "lawyer", 'email': email}
            )
        except ClientError as e:
            logging.error(
                "Couldn't delete lawyer %s. Here's why: %s: %s", email,
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise