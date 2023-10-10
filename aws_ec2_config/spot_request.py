import boto3
import json
import os

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

dir = "/home/nicholas/GitRepos/learn_aws/aws_ec2_config"
with open(os.path.join(dir, "spot_request_config.json")) as oj:
    config = json.load(oj)

ec2_client.request_spot_fleet(
    DryRun=True,
    SpotFleetRequestConfig=config
)
