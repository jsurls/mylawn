from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json

import decimal


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")

table = dynamodb.Table("User")

response = table.scan()
for i in response['Items']:
    print(json.dumps(i, default=decimal_default))
