"""
A script to set up the S3 bucket.

The fastest way to push a whole folder to a s3 bucket is with aws s3 sync.
I have written a wrapper that calls this function from within python. The 
pyaws module will contain helpfull bash wrappers to speed thing up
"""

import boto3
import json
import time 
import wrappers.pyaws as pyaws

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
s3_client = session.client('s3', region_name="us-east-1")
s3_res = session.resource('s3', region_name="us-east-1")

# List all buckets and create the new bucket if not exists
buckets = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]

celeba_bucket = 'celeba-for-tut'
if celeba_bucket not in buckets:
    print('Creating the bucket')
    s3_client.create_bucket(
        Bucket=celeba_bucket,
    )

# add a folder for the images 
bucket = s3_res.Bucket(celeba_bucket)
bucket.put_object(Key="imgs/")

# Push the data to the s3 bucket
rootdir = "/home/nicholas/Datasets/CelebA/img_transformed_100"
pyaws.push_folder_to_s3(
    rootdir=rootdir,
    bucketdir="s3://celeba-for-tut/imgs",
    profile="nick"
)
