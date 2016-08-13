from __future__ import print_function  # Python 2/3 compatibility
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")

try:
    dynamodb.delete_table(
        TableName='User'
    )
except ClientError:
    pass

print("Deleting table.")
