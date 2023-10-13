import boto3
import json
from create_security_group import SecurityGroup


# get the access and secret keys to the aws account
with open("/home/nicholas/GitRepos/OFFLINE/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY_nick']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY_nick']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="us-east-1"
)

ec2_client = session.client("ec2", region_name="us-east-1")

vpc_ids = {}
for vpc in ec2_client.describe_vpcs()['Vpcs']:
    try:
        for tag in vpc['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
    except:
        name = 'NotNamed'
    id = vpc['VpcId']
    vpc_ids[name] = id


sec_group = SecurityGroup(
    vpc_id=vpc_ids['copysteps-vpc'],
    session=session,
)

IpPermissions = [
    {
        'FromPort': 22,
        'IpProtocol': 'tcp',
        'IpRanges': [
            {
                'CidrIp': '0.0.0.0/0',
                'Description': 'Allow SSH from everywhere'
            },
        ],
        'ToPort': 22,
    },
    {
        'FromPort': -1,
        'IpProtocol': 'icmp',
        'IpRanges': [
            {
                'CidrIp': '0.0.0.0/0',
                'Description': 'Allow ping from everywhere'
            },
        ],
        'ToPort': -1,
    },
]

security_group_name = "copystep-sg"
sec_group.create_security_group(
    security_group_name=security_group_name,
    Ip_Permissions=IpPermissions
)
