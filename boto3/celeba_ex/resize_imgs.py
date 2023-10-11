"""
A script to resize all of the celeba images to (3, 64, 64)
"""

import os
from PIL import Image
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
import numpy as np

def transform_folder(
   rootdir,
   transform,
   savedir
   ):

    img_names = os.listdir(rootdir)
    
    for i, img_name in enumerate(img_names):

        if i % 100 == 0:
            print(f"Percent complete {np.round(i / len(img_names), 2)}")

        img = Image.open(os.path.join(rootdir, img_name))
        
        img_t = transform(img)
        
        img_p = transforms.Compose([
            transforms.ToPILImage()
        ])(img_t)
        
        img_p.save(os.path.join(savedir, img_name))

    return None

if __name__ == "__main__":
    rootdir = "/home/nicholas/Datasets/CelebA/img_align_celeba"
    savedir = "/home/nicholas/Datasets/CelebA/img_transformed"
    transform = transforms.Compose([
        transforms.Resize(64),
        transforms.CenterCrop(64),
        transforms.ToTensor()
    ])
    transform_folder(rootdir, transform, savedir)
