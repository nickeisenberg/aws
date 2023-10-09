"""
Create some blobs and then push the blobs to s3 bucket
"""

import boto3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import json

# get the access and secret keys to the aws account
with open("/home/nicholas/GitRepos/password.json") as oj:
    pw = json.load(oj)

ACCESS_KEY = pw['aws_ACCESS_KEY']
SECRET_ACCESS_KEY = pw['aws_SECRET_ACCESS_KEY']

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY
)


