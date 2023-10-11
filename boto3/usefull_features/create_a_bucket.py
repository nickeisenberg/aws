"""
There seem to be some subtileties when creating a bucket.
If you want to create the bucket in us-east-1, the you cant specify the region
in the LocationConstraint in the call below. Apparently it defaults to us-east-1
but at the sametime, if you specify us-east-1 then it throws an error. If you want
to use any other region, then you must specify.
"""

import boto3

ACCESS_KEY = ""
SECRET_ACCESS_KEY = ""


#--------------------------------------------------
# Here is the example for us-east-1
#--------------------------------------------------
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="",
    region_name="us-east-1"
)
s3_client = session.client('s3', region_name="us-east-1")

buckets = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]

celeba_bucket = 'celeba-for-tut'
if celeba_bucket not in buckets:
    print('Creating the bucket')
    s3_client.create_bucket(
        Bucket=celeba_bucket,
    )

#--------------------------------------------------
# Here is the example for any other region
#--------------------------------------------------
region = "some region"
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="",
    region_name=region
)
s3_client = session.client('s3', region_name=region)

buckets = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]

celeba_bucket = 'celeba-for-tut'
if celeba_bucket not in buckets:
    print('Creating the bucket')
    s3_client.create_bucket(
        Bucket=celeba_bucket,
        CreateBucketConfiguration={
            "LocationConstraint": region
        }
    )
