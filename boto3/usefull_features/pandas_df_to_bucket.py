import boto3
import pandas as pd

df = pd.DataFrame()
csv = df.to_csv(index=False)

ACCESS_KEY = ""
SECRET_ACCESS_KEY = ""

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="name_of_region"
)

s3_res = session.resource('s3')

bucket_name = ""
file_path_in_bucket = ""
s3_res.Object(
    bucket_name, 
    file_path_in_bucket
).put(Body=csv)
