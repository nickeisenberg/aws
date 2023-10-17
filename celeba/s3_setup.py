"""
This is to be run on the local machine

A script to set up the S3 bucket.

The fastest way to push a whole folder to a s3 bucket is with aws s3 sync.
I have written a wrapper that calls this function from within python. The 
pyaws module will contain helpfull bash wrappers to speed thing up
"""

import boto3
import json
import pyaws
import time
import pandas as pd
import numpy as np


# get the access and secret keys to the aws account
with open("/home/nicholas/.credentials/password.json") as oj:
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
celeba_bucket = 'celeba-demo-bucket'
if celeba_bucket not in buckets:
    print('Creating the bucket')
    s3_client.create_bucket(
        Bucket=celeba_bucket,
    )

# add a folder for the images 
bucket = s3_res.Bucket(celeba_bucket)
bucket.put_object(Key="parquets/")
bucket.put_object(Key="imgs/")

# Move the file to s3

before_copy = time.time()
source_dir = "/home/nicholas/Datasets/CelebA/img64_pq_1000"
save_dir = "s3://celeba-demo-bucket/parquets/"
profile = "nick"
pyaws.copy_dir(
    source_dir, 
    save_dir,
    profile,
    notify_after=10
)
after_copy = time.time()

print(after_copy - before_copy)

before_sync = time.time()
source_dir = "/home/nicholas/Datasets/CelebA/img64_1000"
save_dir = "s3://celeba-demo-bucket/imgs/"
profile = "nick"
pyaws.sync_dir(
    source_dir, 
    save_dir,
    profile,
    notify_after=10
)
after_sync = time.time()

print(after_sync - before_sync)

df = pd.DataFrame(
    data=[
        ['l-s3', 'pq', np.nan, after_copy - before_copy],
        ['l-s3', 'jpg', after_sync - before_sync, np.nan],
    ],
    columns=['where_to_where', 'what', 'sync', 'cp'],
)

df.to_csv("/home/nicholas/GitRepos/aws/celeba/times.csv")





