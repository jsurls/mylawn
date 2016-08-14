from __future__ import print_function  # Python 2/3 compatibility

import boto3

from config.settings import DYNAMO_LOCAL


def get_user(user_id):
    """ Gets a user from the datastore"""
    table = get_table('User')

    # Create key
    user_id_key = {"id": user_id}

    # Query using key
    response = table.get_item(Key=user_id_key)

    # Return user if one exists
    return response.get('Item', None)


def put_user(user):
    """ Puts a user in the datastore"""
    table = get_table('User')

    # Put user in datastore
    table.put_item(Item=user)


def get_table(table_name):
    """ Gets a Table resource by name"""
    # Get table resource
    if DYNAMO_LOCAL:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    else:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    return dynamodb.Table(table_name)
