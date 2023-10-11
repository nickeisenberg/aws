"""
torchvison.transforms.ToTensor auto scales to [0, 1]
"""

import os
from torchvision import transforms
from PIL import Image

rootdir = "/home/nicholas/Datasets/CelebA/img_transformed_100"
imgs = os.listdir(rootdir)
transform = transforms.Compose([
    transforms.ToTensor()
])
img = Image.open(os.path.join(rootdir, imgs[0]))
img_t = transform(img)
img_t.min()


rootdir = "/home/nicholas/Datasets/CelebA/img_align_celeba"
imgs = os.listdir(rootdir)
transform = transforms.Compose([
    transforms.ToTensor()
])
img = Image.open(os.path.join(rootdir, imgs[0]))
img_t = transform(img)
img_t.max()
