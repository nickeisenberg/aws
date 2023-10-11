"""
Make a small folder of 100 images to test the speeds are various methods of
moving files to S3
"""

import shutil
import os

rootdir = "/home/nicholas/Datasets/CelebA/img_transformed"
files = os.listdir(rootdir)
savedir = "/home/nicholas/Datasets/CelebA/img_transformed_100"

for f in files[: 100]:
    shutil.copy(
        os.path.join(rootdir, f),
        os.path.join(savedir, f),
    )
