from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")

table = dynamodb.Table("User")

with open("../sample/sample_users.json") as json_file:
    users = json.load(json_file)
    for user in users:
        user_id = user['id']
        station_id = user['station_id']
        last_mod = user['last_modification']
        last_invoked = user['last_invoked']
        total_calls = user['total_calls']

        print("Adding user:", user_id)

        table.put_item(
            Item={
                'id': user_id,
                'station_id': station_id,
                'last_mod': last_mod,
                'last_invoked': last_invoked,
                'total_calls': total_calls
            }
        )
