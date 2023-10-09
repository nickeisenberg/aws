#! /bin/bash

# To copy a file from the local computer to the aws s3 bucket, you can run

local_path="<path_to_file>"
bucket_path="<path_to_bucket>"

aws s3 cp $local_path s3://$bucket_path

# Example
# aws s3 cp ~/Downloads/fancy_desk.jpg s3://tempbucket-9229/imgs
