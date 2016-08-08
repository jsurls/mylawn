from __future__ import print_function  # Python 2/3 compatibility

import boto3


def get_user(user_id):
    # Get table resource
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('User')

    # Create key
    user_id_key = {"id": user_id}

    # Query using key
    response = table.get_item(Key=user_id_key)

    # Return user if one exists
    return response.get('Item', None)


def put_user(user):
    # Get table resource
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('User')

    # Put user in datastore
    table.put_item(Item=user)
