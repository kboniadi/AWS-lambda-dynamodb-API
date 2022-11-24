
def generate_lawyers(ddb):
    ddb.create_table(
        TableName='Core',
         KeySchema=[
            {
                'AttributeName': 'category',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'email',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'category',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('Successfully created table Core')

def drop_lawyers(ddb):
    table = ddb.Table('core')
    table.delete()