import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-south-1',
    endpoint_url="http://localhost:8000",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy"
)

table_name = "Users"

try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'username', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'username', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    table.wait_until_exists()
    print("Users table created successfully!")

except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        print("Users table already exists.")
    else:
        print("Unexpected error:", e)