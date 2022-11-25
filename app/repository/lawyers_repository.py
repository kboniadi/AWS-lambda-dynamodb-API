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
        table = self.__db.Table('Core')
        response = table.query(
            KeyConditionExpression=Key('category').eq("lawyer")
        )
        return response.get('Items', [])

    def get_lawyer(self, email: str):
        try:
            table = self.__db.Table('Core')
            response = table.get_item(Key={'category': "lawyer", 'email': email})
            return response['Item']
        except ClientError as e:
            logging.error(
                "Couldn't get lawyer %s. Here's why: %s: %s", email,
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise

    def create_lawyer(self, lawyer: dict):
        table = self.__db.Table('Core')
        response = table.put_item(Item=lawyer)
        return response

    def update_lawyer(self, lawyer: dict):
        table = self.__db.Table('Core')
        response = table.update_item(
            Key={'category': "lawyer", 'email': lawyer.get('email')},
            UpdateExpression="""
                set
                    #email=:email,
                    #title=:title,
                    #name=:name,
                    #languages=:languages,
                    #location=:location,
                    #phone=:phone,
                    #description=:description,
                    #expertise=:expertise
            """,
            ExpressionAttributeValues={
                ':email': lawyer.get('email'),
                ':title': lawyer.get('title'),
                ':name': lawyer.get('name'),
                ':languages': lawyer.get('languages'),
                ':location': lawyer.get('location'),
                ':phone': lawyer.get('phone'),
                ':description': lawyer.get('description'),
                ':expertise': lawyer.get('expertise')
            },
            ExpressionAttributeNames={
                "#email": "email",
                "#title": "title",
                "#name": "name",
                "#lanuages": "lanuages",
                "#location": "location",
                "#phone": "phone",
                "#description": "description",
                "#expertise": "expertise",
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_lawyer(self, email: str):
        try:
            table = self.__db.Table('Core')
            response = table.delete_item(
                Key={'category': "lawyer", 'email': email}
            )
            return response
        except ClientError as e:
            logging.error(
                "Couldn't delete lawyer %s. Here's why: %s: %s", email,
                e.response['Error']['Code'], e.response['Error']['Message'])
            raise