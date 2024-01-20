import subprocess
import schedule
from botocore.exceptions import ClientError
import time
import boto3
import json

# Create an EC2 resource object using the session
client = boto3.client(service_name='secretsmanager',
                      region_name='us-east-1')
response = client.get_secret_value(
    SecretId='secrets'
)
secret = response['SecretString']
secret_access_keys = json.loads(secret)

ec2 = boto3.Session(
    aws_access_key_id=secret_access_keys['access_key_id'],
    aws_secret_access_key=secret_access_keys['secret_access_key'],
    region_name='us-east-1'
    ).resource('ec2')

# Specify the ID of the instance you want to start/stop - replace this with your instance id
instance_id = 'i-0776930ba52bea8a5'

def invoke_smart_doctor_inference_job():
    try:
        # Start the instance
        instance = ec2.Instance(instance_id)
        instance.start()
        instance.wait_until_running()
        time.sleep(60) # Wait for the instance to start

        # Execute the orchestrator.py script
        ssh_command = 'ssh -i /home/ubuntu/key.pem ubuntu@{} python3 /home/ubuntu/smart_doctor/orchestrator.py >> smart_doctor.log'.format(instance.public_dns_name)
        process = subprocess.Popen(ssh_command, stdout=subprocess.PIPE, shell=True)
        process.communicate()
        
        # Stop the instance
        ec2.Instance(instance_id).stop()
        print('Instance stopped')

    except ClientError as e:
        print("Unexpected error: %s" % e)

schedule.every().day.at("18:30").do(invoke_smart_doctor_inference_job)  # replace '10:30' with your preferred time

while True:
    schedule.run_pending()
    time.sleep(10) 
