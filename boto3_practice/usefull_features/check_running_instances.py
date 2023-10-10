import boto3
import json

# get the access and secret keys to the aws account
with open("/home/nicholas/GitRepos/OFFLINE/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

# start the session
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="us-east-1"
)

# create the resource and the client
ec2_client = session.client("ec2", region_name="us-east-1")

"""
The command
ec2_client.describe_instances()['Reservations']
produces a list where each item in the list represents a different instance 
"""

all_instances = []
all_instances_ids = []
for inst in ec2_client.describe_instances()['Reservations']:
    all_instances_ids.append(inst['Instances'][0]['InstanceId'])
    for tag in inst['Instances'][0]['Tags']:
        if tag['Key'] == 'Name':
            all_instances.append(tag['Value'])

print(all_instances)
print(all_instances_ids)
