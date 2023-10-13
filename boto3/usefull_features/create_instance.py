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

# First lets get all EC2 instances
all_instances = []
all_instances_ids = []
for inst in ec2_client.describe_instances()['Reservations']:
    all_instances_ids.append(inst['Instances'][0]['InstanceId'])
    for tag in inst['Instances'][0]['Tags']:
        if tag['Key'] == 'Name':
            all_instances.append(tag['Value'])

instance_config = {
  "MaxCount": 1,
  "MinCount": 1,
  "ImageId": "ami-053b0d53c279acc90",
  "InstanceType": "t2.micro",
  "KeyName": "us-east-1-kp",
  "EbsOptimized": False,
  "BlockDeviceMappings": [
    {
      "DeviceName": "/dev/sda1",
      "Ebs": {
        "Encrypted": False,
        "DeleteOnTermination": True,
        "SnapshotId": "snap-0d3283808e9f92122",
        "VolumeSize": 15,
        "VolumeType": "gp3"
      }
    },
  ],
  "NetworkInterfaces": [
    {
      "AssociatePublicIpAddress": True,
      "DeviceIndex": 0,
      "Groups": [
        "sg-0359d7d29e84ece55"
      ]
    }
  ],
  "TagSpecifications": [
    {
      "ResourceType": "instance",
      "Tags": [
        {
          "Key": "Name",
          "Value": "testec2"
        }
      ]
    }
  ],
  "PrivateDnsNameOptions": {
    "HostnameType": "ip-name",
    "EnableResourceNameDnsARecord": True,
    "EnableResourceNameDnsAAAARecord": False
  }
}

# Lets create the instance "cluster-example" f the instance is not already 
# created
instance = ec2_res.create_instances(**instance_config)

all_instances = []
all_instances_ids = []
for inst in ec2_client.describe_instances()['Reservations']:
    all_instances_ids.append(inst['Instances'][0]['InstanceId'])
    for tag in inst['Instances'][0]['Tags']:
        if tag['Key'] == 'Name':
            all_instances.append(tag['Value'])

ec2_client.describe_instances()['Reservations'][0]['Instances'][0]['PublicIpAddress']

