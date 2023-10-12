"""
Create a volume and test if its available
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
    profile_name="nick",
    region_name="us-east-1"
)

# create the resource and the client
ec2_res = session.resource('ec2')
ec2_client = session.client("ec2", region_name="us-east-1")

volume_config = {
    "AvailabilityZone": 'us-east-1a',
    "Encrypted": False,
    "Iops": 150,  # baseline is IOPS = 3 * size with a min of 100
    "Size": 50, # In GiB
    "VolumeType": 'gp3',
    "DryRun": False,
    "TagSpecifications": [
        {
            "ResourceType": "volume",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "testvolname"
                },
            ]
        },
    ],
    "MultiAttachEnabled": False,
    "Throughput": 125,  # Only applicable for gp3. Min is 125 MiB/s and max is 1000
}

response = ec2_client.create_volume(**volume_config)

if response['ResponseMetadata']['HTTPStatusCode']== 200:
       volume_id= response['VolumeId']
       print('***volume:', volume_id)

       ec2_client.get_waiter('volume_available').wait(
           VolumeIds=[volume_id],
           DryRun=False
           )

       print('***Success!! volume:', volume_id, 'created...')

