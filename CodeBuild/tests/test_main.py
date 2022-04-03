import unittest
import boto3
import random
import main

DYNAMODB_REGION_NAME = 'ap-northeast-1'
DYNAMODB_ENDPOINT_URL = 'http://localhost:8000'
ACCESS_KEY_ID = 'dummy_access_key_id'
SECRET_ACCESS_KEY = 'dummy_secret_access_key'
TABLE_NAME = 'example_table'

class TestMain(unittest.TestCase):
    dynamodb = None

    @classmethod
    def setUpClass(cls):
        global dynamodb
        dynamodb = boto3.client(
            'dynamodb',
            DYNAMODB_REGION_NAME,
            endpoint_url = DYNAMODB_ENDPOINT_URL,
            aws_access_key_id = ACCESS_KEY_ID,
            aws_secret_access_key = SECRET_ACCESS_KEY
        )
        cls.__create_example_table(dynamodb)

    @classmethod
    def __create_example_table(cls, dynamodb):
        try:
            dynamodb.create_table(
                TableName = TABLE_NAME,
                KeySchema = [
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions = [
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'N'
                    }
                ],
                ProvisionedThroughput = {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
        except dynamodb.exceptions.ResourceInUseException:
            pass


    def test_save_dynamodb_record(self):
        ## given
        id = str(random.randint(1, 10))
        name = 'name_' + id

        ## when
        main.save_dynamodb_record(
            dynamodb,
            TABLE_NAME,
            id,
            name
        )

        ## then
        create_record = dynamodb.get_item(
            TableName = TABLE_NAME,
            Key = {'id' : {'N' : id}}
        )['Item']
        self.assertEqual(create_record['id']['N'], id)
        self.assertEqual(create_record['name']['S'], name)


    @classmethod
    def tearDownClass(cls):
        dynamodb.delete_table(
            TableName = TABLE_NAME
        )