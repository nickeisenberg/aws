"""
A script to resize all of the celeba images to (3, 64, 64)
"""

import os
from PIL import Image
from torchvision import transforms
import numpy as np
import shutil

def transform_folder(
    rootdir,
    transform,
    savedir,
    make_small_test_dir=True,
    ):

    img_names = os.listdir(rootdir)
    
    for i, img_name in enumerate(img_names):

        if i % 250 == 0:
            print(f"Percent complete {np.round(100 * i / len(img_names), 3)}")

        img = Image.open(os.path.join(rootdir, img_name))
        
        img_t = transform(img)

        img_t.save(os.path.join(savedir, img_name))
    
    if make_small_test_dir:
        print("Making the small test directory")
        small_test_dir = savedir + "_100"
        
        try:
            os.makedirs(small_test_dir)
        except:
            pass

        for i, img_name in enumerate(img_names):
            shutil.copy(
                os.path.join(savedir, img_name),
                os.path.join(small_test_dir, img_name)
            )
            if i > 100:
                break

    return None

if __name__ == "__main__":
    rootdir = "/home/nicholas/Datasets/CelebA/img_align_celeba"
    savedir = "/home/nicholas/Datasets/CelebA/img_64"
    transform = transforms.Compose([
        transforms.Resize(64),
        transforms.CenterCrop(64)
    ])
    transform_folder(rootdir, transform, savedir)



