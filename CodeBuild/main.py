import boto3
import sys

DYNAMODB_REGION_NAME = 'ap-northeast-1'
TABLE_NAME = 'example_table'

def initialize_dynamodb(region_name):
    return boto3.client(
        'dynamodb',
        region_name = region_name
    )

def save_dynamodb_record(dynamodb, table_name, id, name):
    dynamodb.put_item(
        TableName = table_name,
        Item = {
            'id' : {'N' : id},
            'name' : {'S' : name}
        }
    )

if __name__ == "__main__":
    dynamodb = initialize_dynamodb(DYNAMODB_REGION_NAME)
    args = sys.argv
    save_dynamodb_record(
        dynamodb,
        TABLE_NAME,
        args[1],
        args[2],
    )