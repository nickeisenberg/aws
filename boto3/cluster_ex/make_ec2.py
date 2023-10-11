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
with open("/home/nicholas/GitRepos/OFFLINE/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

# start the session
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    # profile_name="",
    region_name="us-east-2"
)

# create the resource and the client
ec2_res = session.resource('ec2')
ec2_client = session.client("ec2", region_name="us-east-2")

# Create the instance 

# Here is the ami id for ubuntu that will be needed to create the instance 
# Ubuntu 22.04
#us-east-2
ami = "ami-024e6efaf93d85776"

# First lets get all EC2 instances
all_instances = []
for x in ec2_client.describe_instances()['Reservations'][0]['Instances']:
    for tag in x['Tags']:
        if tag['Key'] == 'Name':
            all_instances.append(tag['Value'])

# Lets create the instance "cluster-example" f the instance is not already 
# created
if "cluster-example" not in all_instances:
    print("Creating the instance")
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

# Verif that the instance is there now
ec2_client.describe_instances()['Reservations'][0]['Instances'][0]['Tags']

# Here is the public ip_address so that we can SSH into the instance 
ec2_client.describe_instances()['Reservations'][0]['Instances'][0]['PublicIpAddress']

# Now lets take this and ssh into the instance. We will now move to the script
# ssh_to_ec2.py
