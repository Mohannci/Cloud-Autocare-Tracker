import boto3
from django.conf import settings
from uuid import uuid4
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    region_name=settings.AWS_DYNAMODB_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token=settings.AWS_SESSION_TOKEN
)

# Table references
users_table = dynamodb.Table('Users')
vehicles_table = dynamodb.Table('Vehicles')
records_table = dynamodb.Table('MaintenanceRecords')

def create_user(username, password_hash):
    try:
        users_table.put_item(Item={'username': username, 'password_hash': password_hash})
        return True
    except ClientError as e:
        print(f"Error creating user: {e}")
        return False

def get_user(username):
    try:
        response = users_table.get_item(Key={'username': username})
        return response.get('Item')
    except ClientError as e:
        print(f"Error retrieving user: {e}")
        return None

def create_vehicle(user_id, vehicle_name, model, year):
    try:
        vehicle_id = str(uuid4())
        vehicles_table.put_item(Item={
            'vehicle_id': vehicle_id,
            'user_id': user_id,
            'vehicle_name': vehicle_name,
            'model': model,
            'year': year
        })
        return vehicle_id
    except ClientError as e:
        print(f"Error creating vehicle: {e}")
        return None

def get_vehicles(user_id):
    try:
        response = vehicles_table.scan(FilterExpression='user_id = :uid', ExpressionAttributeValues={':uid': user_id})
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error retrieving vehicles: {e}")
        return []

def update_vehicle(vehicle_id, user_id, vehicle_name, model, year):
    try:
        vehicles_table.update_item(
            Key={'vehicle_id': vehicle_id},  # Use only vehicle_id as the key
            UpdateExpression='SET #vn = :v, #m = :mo, #y = :y',
            ExpressionAttributeNames={'#vn': 'vehicle_name', '#m': 'model', '#y': 'year'},
            ConditionExpression='user_id = :uid',  # Ensure the item belongs to the user
            ExpressionAttributeValues={
                ':v': vehicle_name,
                ':mo': model,
                ':y': year,
                ':uid': user_id  # Combine all values in one dictionary
            }
        )
        return True
    except ClientError as e:
        print(f"Error updating vehicle: {e}")
        return False

def delete_vehicle(vehicle_id, user_id):
    try:
        vehicles_table.delete_item(
            Key={'vehicle_id': vehicle_id},  # Use only vehicle_id as the key
            ConditionExpression='user_id = :uid',  # Ensure the item belongs to the user
            ExpressionAttributeValues={':uid': user_id}
        )
        return True
    except ClientError as e:
        print(f"Error deleting vehicle: {e}")
        return False

def create_maintenance_record(vehicle_id, service_date, description, cost):
    try:
        record_id = str(uuid4())
        records_table.put_item(Item={
            'record_id': record_id,
            'vehicle_id': vehicle_id,
            'service_date': service_date,
            'description': description,
            'cost': Decimal(str(cost))
        })
        return record_id
    except ClientError as e:
        print(f"Error creating maintenance record: {e}")
        return None

def get_maintenance_records(vehicle_id):
    try:
        response = records_table.scan(FilterExpression='vehicle_id = :vid', ExpressionAttributeValues={':vid': vehicle_id})
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error retrieving maintenance records: {e}")
        return []