import os
from PIL import Image
from torchvision import transforms
import numpy as np
import matplotlib.pyplot as plt
import pyarrow as pa
import pyarrow.parquet as pq


def to_parquet(
    transform,
    rootdir,
    savedir,
    notify_afer = 1
    ):

    """
    Transforms all images in a folder to parquet files. The columns of the 
    parquet tables correspond to the channels in the image. Each image gets its
    own parquet file.
    
    Note
    ----
    To reconstrut the image, use the following
    
    table = pq.read_table("<path_to_table>")
    np.array([table[f"ch{i}"].to_numpy().reshape((64, 64)) for i in [0, 1, 2]])
    """

    img_names = os.listdir(rootdir)
    ch_names = [f"ch{i}" for i in [0, 1, 2]]
    for i, img_name in enumerate(img_names[: 10]):

        if i % notify_afer == 0:
            print(f"PERCENT COMPLETE: {np.round(100 * i / len(img_names), 2)}")
        # PIL image
        img = Image.open(os.path.join(rootdir, img_name))

        # PIL to numpy array (3, 64, 64)
        img_t = transform(img).numpy()

        ch_arrs = [arr.reshape(-1) for arr in img_t]

        table = pa.Table.from_arrays(
            ch_arrs, ch_names
        )

        pq_name = img_name.split('.')[0] + ".pq"
        pq.write_table(
            table, 
            os.path.join(savedir, pq_name)
        )

    return None


rootdir = "/home/nicholas/Datasets/CelebA/img_align_celeba"
savedir = "/home/nicholas/Datasets/CelebA/img_64_parquet"
transform = transforms.Compose(
    [
        transforms.Resize(64),
        transforms.CenterCrop(64),
        transforms.ToTensor()
    ]
)

to_parquet(
    transform,
    rootdir,
    savedir,
    notify_afer=1
)


# Test the reconstruction
img_names = os.listdir(rootdir)
pqnames = os.listdir(savedir)

print(img_names[:10])
print(pqnames)

img = Image.open(os.path.join(rootdir, img_names[4]))
img_t = transform(img).numpy()
table = pq.read_table(os.path.join(savedir, pqnames[0]))
for i, arr in enumerate(
    np.array([table[f"ch{i}"].to_numpy().reshape((64, 64)) for i in [0, 1, 2]])
):
    print((arr != img_t[i]).sum())
