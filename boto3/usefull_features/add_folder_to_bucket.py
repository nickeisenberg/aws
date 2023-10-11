import boto3

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
bucket = s3_res.Bucket(bucket_name)

new_folder = "name_of_folder/"  # The / is important
bucket.put_object(Key=new_folder)
