import boto3

ACCESS_KEY = ""
SECRET_ACCESS_KEY = ""

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    profile_name="",
    region_name=""
)
s3_client = session.client('s3', region_name="")

BUCKET = ''
PREFIX = ''
response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX)
for object in response['Contents']:
    print('Deleting', object['Key'])
    s3_client.delete_object(Bucket=BUCKET, Key=object['Key'])
