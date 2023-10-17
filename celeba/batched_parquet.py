import os
from PIL import Image
from torchvision import transforms
import numpy as np
import matplotlib.pyplot as plt
import pyarrow as pa
import pyarrow.parquet as pq

def to_batched_parquet(
    transform: transforms.Compose,
    rootdir,
    savedir,
    im_per_batch=10,
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
    arrs = []
    batch_num = 0
    arr_names = []
    for i, img_name in enumerate(img_names):

        # PIL image
        img = Image.open(os.path.join(rootdir, img_name))
    
        img_t = transform(img)

        try:
            # PIL to numpy array
            img_t = img_t.numpy()

        except:
            print("The transformed image could not be transformed into a numpy array")
            return None

        flattened_img = img_t.reshape(-1)

        arrs.append(flattened_img)
        arr_names.append(img_name)
        
        if (i + 1) % im_per_batch == 0:

            batch_num += 1

            table = pa.Table.from_arrays(
                arrs, arr_names
            )

            pq.write_table(
                table, 
                os.path.join(savedir, f"batch{batch_num}")
            )

            percent_complete = np.round(100 * (batch_num * im_per_batch) / len(img_names), 2)
            print(f"BATCH {batch_num} PERCENT COMPLETE {percent_complete}")

            arrs = []
            arr_names = []

    return None


rootdir = "/home/nicholas/Datasets/CelebA/img_align_celeba_10000"
savedir = "/home/nicholas/Datasets/CelebA/batched"
transform = transforms.Compose(
    [
        transforms.Resize(64),
        transforms.CenterCrop(64),
        transforms.ToTensor()
    ]
)

to_batched_parquet(transform, rootdir, savedir, im_per_batch=100)


pq_paths = [os.path.join(savedir, name) for name in os.listdir(savedir)]

table = pq.read_table(pq_paths[0])

table.column_names

img = table["000824.jpg"].to_numpy()

img = img.reshape((3, 64, 64))
