"""
Create an ubuntu 22.04 instance.

Usefull links

1) Creating a EC2 instance within boto3
https://saturncloud.io/blog/how-to-create-an-ec2-instance-using-boto3-a-comprehensive-guide-for-data-scientists/

2) Another way to create an EC2 instance
https://stackoverflow.com/questions/32863768/how-to-create-an-ec2-instance-using-boto3

3) boto3 docs on creating an instance
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_instances.html

4)
Give a name to the instance from boto3
https://stackoverflow.com/questions/57585019/boto3-ec2-create-instance-with-a-name

5) Some troubleshooting in case your account is blocked
https://stackoverflow.com/questions/46649542/aws-ec2-cant-launch-an-instance-account-blocked
"""

import boto3
import json

# get the access and secret keys to the aws account
with open("/home/nicholas/GitRepos/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY']

# start the session
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name="us-east-2"
)

# create the resource 
ec2_res = session.resource('ec2')

# Here is the ami id for ubuntu
# Ubuntu 22.04
#us-east-2
ami = "ami-024e6efaf93d85776"

# Create the instance 
instance = ec2_res.create_instances(
    ImageId=ami,
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName="cluster-example-kp",
    SecurityGroupIds=["sg-05814cf24f8edfd23"], # us-east-2
    SecurityGroups=["cluster-example-sg"],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'cluster-example'
                },
            ]
        },
    ],
)

# Check if the instance is running
ec2_client = boto3.client("ec2", region_name="us-east-2")
ec2_client.describe_instances()['Reservations'][0]['Instances'][0]['Tags']

