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


security_group_name = "copysteps-sg"
vpc_id = vpc_ids['copysteps-vpc']
dryrun=False

sg_config = {
    "Description": 'Created from the boto wrapper',
    "GroupName": security_group_name,
    "VpcId": vpc_id,
    "DryRun": dryrun 
}

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
ingress_config = {
    "IpPermissions": IpPermissions,
    "DryRun": dryrun,
}
egress_config = {
    "IpPermissions": IpPermissions,
    "DryRun": dryrun,
}

sec_group = SecurityGroup(
    vpc_id=vpc_id,
    session=session,
)

sec_group.create_security_group(
    sg_config,
    ingress_config,
    egress_config
)

sec_group._add_rules_to_security_group(
    "copysteps-sg",
    ingress_config,
    egress_config
)
