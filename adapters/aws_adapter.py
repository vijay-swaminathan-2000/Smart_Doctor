import boto3
from botocore.exceptions import NoCredentialsError
import json

def get_secret(secret_name):
    client = create_boto3_session().client(service_name='secretsmanager', region_name='us-east-1')

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except NoCredentialsError:
        print("Unable to locate AWS credentials.")
        return None
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret with name '{secret_name}' not found.")
        return None
    except client.exceptions.ClientError as e:
        print(f"Error occurred while retrieving secret '{secret_name}': {e.response['Error']['Message']}")
        return None

    if 'SecretString' in response:
        secret_value = response['SecretString']
    else:
        print("Secret value not found.")
        return None

    return secret_value

def get_secret_access_keys():
    client = boto3.client(service_name='secretsmanager',
                      region_name='us-east-1')

    response = client.get_secret_value(
        SecretId='secrets'
    )

    secret = response['SecretString']
    return json.loads(secret)

def create_boto3_session():
    # Create a session using your AWS credentials
    secret_access_keys = get_secret_access_keys()
    session = boto3.Session(
    aws_access_key_id=secret_access_keys['access_key_id'],
    aws_secret_access_key=secret_access_keys['secret_access_key'],
    region_name='us-east-1'
    )
    return session