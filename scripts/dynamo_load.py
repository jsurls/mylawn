from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:4569")

table = dynamodb.Table("User")

with open("sample/sample_users.json") as json_file:
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

print("Loaded: User")

table = dynamodb.Table("GeoLookup")

with open("sample/sample_geolookup.json") as json_file:
    stations = json.load(json_file)
    for station in stations:
        zipcode = station['id']
        station_id = user['station_id']

        print("Adding zipcode:", zipcode)

        table.put_item(
            Item={
                'id': zipcode,
                'station_id': station_id
            }
        )

print("Loaded: GeoLocation")
