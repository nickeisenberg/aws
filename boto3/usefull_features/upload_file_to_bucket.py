import boto3

ACCESS_KEY = ""
SECRET_ACCESS_KEY = ""

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="nick",
    region_name="name_of_region"
)

s3_client = session.client('s3')

path_to_file_local = ""
bucket_name = ""
file_name_on_bucket = ""
s3_client.upload_file(
    path_to_file_local, 
    bucket_name, 
    file_name_on_bucket
)
