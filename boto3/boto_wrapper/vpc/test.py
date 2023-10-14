import boto3
import json

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

client = session.client("ec2", region_name="us-east-1")

#--------------------------------------------------
vpc_config = {
    "CidrBlock": '10.0.0.0/16',
    "TagSpecifications": [
        {
            'ResourceType': 'vpc',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'newvpc'
                },
            ]
        },
    ]
}
response = client.create_vpc(
    **vpc_config
)
vpcid = response['Vpc']['VpcId']
#--------------------------------------------------


#--------------------------------------------------
igw_config = {
    "TagSpecifications": [
        {
            'ResourceType': 'internet-gateway',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'newvpc-igw'
                },
            ]
        },
    ],
    "DryRun": False
}
igw_response = client.create_internet_gateway(
    **igw_config
)
igw_id = igw_response['InternetGateway']['InternetGatewayId']
#--------------------------------------------------


#--------------------------------------------------
session.resource('ec2').Vpc(vpcid).attach_internet_gateway(
    InternetGatewayId=igw_id
)
#--------------------------------------------------

#--------------------------------------------------
subnet_config = {
    "TagSpecifications": [
        {
            "ResourceType": "subnet",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "newvpc-public-1a"
                },
            ]
        }
    ],
    "AvailabilityZone": "us-east-1a",
    "CidrBlock": "10.0.0.0/16",
    "VpcId": vpcid
}
session.resource('ec2').Vpc(vpcid).create_subnet(**subnet_config)
#--------------------------------------------------

#--------------------------------------------------
rt_config = {
    "VpcId": vpcid,
    "TagSpecifications": [
        {
            'ResourceType': 'route-table',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'newvpc-rtb'
                },
            ]
        },
    ]
}
response = client.create_route_table(**rt_config)
rt_id = response['RouteTable']['RouteTableId']
#--------------------------------------------------

#--------------------------------------------------
cr_config = {
    "DestinationCidrBlock": '0.0.0.0/0',
    "GatewayId": igw_id,
    "RouteTableId": rt_id,
}
response = client.create_route(**cr_config)
#--------------------------------------------------

#--------------------------------------------------
art_config = {
    "RouteTableId": rt_id,
    "SubnetId": 'subnet-07d25cfc5b28f8af9',
}
response = client.associate_route_table(**art_config)
#--------------------------------------------------
