"""
This is to be run on the ec2 instance
"""

import pyaws

source_dir = "s3://celeba-demo-bucket/parquets/"
save_dir = "/data/parquets"
profile = "nick"

pyaws.sync_dir_to_s3(
    source_dir, 
    save_dir,
    profile,
    notify_after=1
)
