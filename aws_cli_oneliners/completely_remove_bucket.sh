#! /bin/bash

# This is supposed to remove a bucket. Seems to be some issues.
# Still need to investigate

buckek_name=""

# emptys the bucket
aws s3 rm s3://$buckek_name --recursive

# remove all versioned objectes
aws s3api delete-objects \
    --bucket $buckek_name \
    --delete "$(aws s3api list-object-versions \
    --bucket $buckek_name \
    --query='{Objects: Versions[].{Key:Key,VersionId:VersionId}}')"

# delete the bucket
aws s3 rb s3://$buckek_name
