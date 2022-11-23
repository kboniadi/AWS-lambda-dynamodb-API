
def generate_lawyers(ddb):
    ddb.create_table(
        TableName='Lawyers',
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('Successfully created table Lawyers')

def drop_lawyers(ddb):
    table = ddb.Table('Lawyers')
    table.delete()