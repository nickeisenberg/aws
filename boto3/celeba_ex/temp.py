"""
torchvison.transforms.ToTensor auto scales to [0, 1]
"""

import os
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt

rootdir = "/home/nicholas/Datasets/CelebA/img_64_100"
imgs = os.listdir(rootdir)

transform = transforms.Compose([
    transforms.PILToTensor()
])

img = Image.open(os.path.join(rootdir, imgs[0]))
img_t = transform(img)

img_t.shape
img_t.min()
img_t.max()

