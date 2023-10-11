import boto3
import json
import os
import time 
import numpy as np

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

buckets = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]

celeba_bucket = 'celeba-for-tut'
if celeba_bucket not in buckets:
    print('Creating the bucket')
    s3_client.create_bucket(
        Bucket=celeba_bucket,
    )

bucket = s3_res.Bucket(celeba_bucket)
bucket.put_object(Key="celeba_imgs/")

rootdir = "/home/nicholas/Datasets/CelebA/img_transformed"
files = os.listdir(rootdir)

start = time.time()
for i in range(100):
    if i % 20 == 0:
        print(f"Percent Complete {np.round(100 * i / 100, 2)}")
    s3_client.upload_file(
        os.path.join(rootdir, files[i]), 
        celeba_bucket, 
        os.path.join("celeba_imgs", files[i])
    )
end = time.time()
"""
This took 20 seconds for 100 images
"""
