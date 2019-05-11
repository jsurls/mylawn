import boto3
import os
import logging

DYNAMO_LOCAL = os.getenv('DYNAMO_LOCAL', 'True')

# Setup basic logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def get_user(user_id):
    """ Gets a user from the datastore"""
    return key_lookup('User', user_id)


def put_user(user):
    """ Puts a user in the datastore"""
    table = get_table('User')

    # Put in datastore
    table.put_item(Item=user)


def get_geolookup(zipcode):
    """ Gets a default station id for this zipcode"""
    return key_lookup('GeoLookup', zipcode)


def put_geolookup(geolookup):
    """ Puts a user in the datastore"""
    table = get_table('GeoLookup')

    # Put in datastore
    table.put_item(Item=geolookup)


def key_lookup(tablename, key):
    """ Gets a value from table given key"""
    table = get_table(tablename)

    # Create key
    k = {"id": key}

    # Query using key
    response = table.get_item(Key=k)

    # Return user if one exists
    return response.get('Item', None)


def get_table(table_name):
    """ Gets a Table resource by name"""
    # Get table resource
    if DYNAMO_LOCAL == 'True':
        logging.warn("Using LOCAL DYNAMO DB! - %s", DYNAMO_LOCAL)
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:4569")
    else:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    return dynamodb.Table(table_name)
