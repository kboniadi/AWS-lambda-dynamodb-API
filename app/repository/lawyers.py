from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource

class LawyersRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db

    def get_all(self):
        table = self.__db.Table('Lawyers')
        response = table.scan()
        return response.get('Items', [])

    def get_lawyer(self, uid: str):
        try:
            table = self.__db.Table('Lawyers')
            response = table.get_item(Key={'uid': uid})
            return response['Item']
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_lawyer(self, lawyer: dict):
        table = self.__db.Table('Lawyers')
        response = table.put_item(Item=lawyer)
        return response

    def update_lawyer(self, lawyer: dict):
        table = self.__db.Table('Lawyers')
        response = table.update_item(
            Key={'uid': lawyer.get('uid')},
            UpdateExpression="""
                set
                    #title=:title,
                    #name=:name,
                    #location=:location,
                    #phone=:phone,
                    #description=:description,
                    #expertise=:expertise
            """,
            ExpressionAttributeValues={
                ':title': lawyer.get('title'),
                ':name': lawyer.get('name'),
                ':location': lawyer.get('location'),
                ':phone': lawyer.get('phone'),
                ':description': lawyer.get('description'),
                ':expertise': lawyer.get('expertise')
            },
            ExpressionAttributeNames={
                "#title": "title",
                "#name": "name",
                "#location": "location",
                "#phone": "phone",
                "#description": "description",
                "#expertise": "expertise",
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_lawyer(self, uid: str):
        table = self.__db.Table('Lawyers')
        response = table.delete_item(
            Key={'uid': uid}
        )
        return response