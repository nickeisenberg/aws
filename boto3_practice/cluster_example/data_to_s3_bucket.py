"""
Create some blobs and then push the blobs to s3 bucket

Some helpfull links:

1) Creating a bucket
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/create_bucket.html

2) Adding a folder to a s3 bucket.
https://saturncloud.io/blog/how-to-create-a-folder-in-amazon-s3-using-boto3/

3) Adding pandas data frames to a s3 bucket as csv files.
https://saturncloud.io/blog/writing-pandas-dataframes-to-s3-buckets-in-aws-a-comprehensive-guide/

4) Uploadng files to a bucket
https://saturncloud.io/blog/how-to-upload-to-amazon-s3-using-boto3-and-return-public-url/

5) Reading a csv from a s3 bucket into memory
https://saturncloud.io/blog/read-and-parse-csv-files-in-s3-without-downloading-the-entire-file-using-python/

6) Downloading a file to local storage from a s3 bucket
https://realpython.com/python-boto3-aws-s3/#downloading-a-file
"""

import boto3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import json

# get the access and secret keys to the aws account
with open("/home/nicholas/GitRepos/OFFLINE/password.json") as oj:
    pw = json.load(oj)

"""
Blob creation
"""
blobs = np.random.normal(
    size=(1000, 2)
)
blobs[:500] += np.array([5, 5])

labels = np.zeros(1000)
labels[500:] += 1

plt.scatter(
    blobs[:, 0], blobs[:, 1]
)
plt.show()

df = pd.DataFrame(
    data=np.hstack((labels.reshape((-1, 1)), blobs))
).set_axis(['labels', 'x', 'y'], axis=1)

csv_0 = df.iloc[:500].to_csv(index=False)
csv_1 = df.iloc[500:].to_csv(index=False)

"""
Moving the blobs to a aws s3 bucket
"""

ACCESS_KEY = pw['aws_ACCESS_KEY']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY
)

# Create a s3 client that can make s3 buckets
s3_client = boto3.client('s3')

# here are all the buckets
buckets = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]

# add this bucket if it does not exist
new_bucket = 'my-boto3-practice'
if new_bucket not in buckets:
    print('Creating the bucket')
    s3_client.create_bucket(Bucket=new_bucket)

# create the s3 resource that can add to an existing bucket
s3_res = boto3.resource('s3')

# First lets connect to the new bucket and get all of the existing objects.
# This includes folders and individual files.
bucket = s3_res.Bucket(new_bucket)
all_objects = [x.key for x in list(bucket.objects.all())]

# Lets create this new directory if it does not already exist
new_dir = "clusters/"
if new_dir not in all_objects:
    print("creating the new folder")
    bucket.put_object(Key=new_dir)
    
# With the new folder created, we can now add the cluster csv's to the folder
s3_res.Object(new_bucket, new_dir + "cluster_0.csv").put(Body=csv_0)
s3_res.Object(new_bucket, new_dir + "cluster_1.csv").put(Body=csv_1)

# We can see if they were in fact added
print([x.key for x in list(bucket.objects.all())])

# If the files were on the computer then we can do the following to upload to a 
# bucket. The following is just for show
path_to_file_local = ""
file_name_on_bucket = ""
s3_client.upload_file(
    path_to_file_local, new_bucket, file_name_on_bucket
)

# We can also read these files back into memory
data = s3_client.get_object(
    Bucket=new_bucket, 
    Key=new_dir + "cluster_0.csv"
)['Body'].read().decode("utf-8")

parsed_csv_0 = pd.read_csv(io.StringIO(data))

# All looks good
print(parsed_csv_0.head())
print(parsed_csv_0.tail())

# We can also download the file
s3_res.Object(
    new_bucket, 
    new_dir + "cluster_0.csv"
).download_file(
    '/home/nicholas/GitRepos/learn_aws/boto3_practice/cluster_example/cluster_0.csv'
)
