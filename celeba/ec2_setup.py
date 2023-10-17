"""
This is to be run on the ec2 instance
"""

import pyaws
import pandas as pd
import numpy as np
import time

before_sync = time.time()
source_dir = "s3://celeba-demo-bucket/parquets/"
save_dir = "/data/parquets"
profile = "nick"
pyaws.sync_dir(
    source_dir, 
    save_dir,
    profile,
    notify_after=10
)
after_sync = time.time()



before_copy = time.time()
source_dir = "s3://celeba-demo-bucket/imgs/"
save_dir = "/data/imgs"
profile = "nick"
pyaws.copy_dir(
    source_dir, 
    save_dir,
    profile,
    notify_after=10
)
after_copy = time.time()

df = pd.DataFrame(
    data=[
        ['s3-ec2', 'jpg', np.nan, after_copy - before_copy],
        ['s3-ec2', 'pq', after_sync - before_sync, np.nan],
    ],
    columns=['where_to_where', 'what', 'sync', 'cp'],
)

df.to_csv("/home/ubuntu/times.csv")
