import os
from PIL import Image
from torchvision import transforms
import numpy as np
import gzip
import blosc
import pickle

def to_batched_npy(
    transform: transforms.Compose,
    rootdir,
    savedir,
    im_per_batch=10
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

            pickled_arrs = pickle.dumps(np.array(arrs))
            compressed_pickle = blosc.compress(pickled_arrs)
           
            with open(os.path.join(savedir, f"batch{batch_num}.dat"), "wb") as f:
                f.write(compressed_pickle)

            # zipped_imgs = gzip.GzipFile(
            #     os.path.join(savedir, f"batch{batch_num}.npy.gz"), 
            #     "w"
            # )
            # np.save(file=zipped_imgs, arr=arrs)
            # zipped_imgs.close()
            
            # arr_names = np.array(arr_names)
            # zipped_names = gzip.GzipFile(
            #     os.path.join(savedir, f"batch{batch_num}_names.npy.gz"), 
            #     "w"
            # )
            # np.save(file=zipped_names, arr=arrs)
            # zipped_names.close()

            percent_complete = np.round(100 * (batch_num * im_per_batch) / len(img_names), 2)
            print(f"BATCH {batch_num} PERCENT COMPLETE {percent_complete}")

            arrs = []
            arr_names = []

    return None


rootdir = "/home/nicholas/Datasets/CelebA/img_align_celeba_10000"
savedir = "/home/nicholas/Datasets/CelebA/numpy"
transform = transforms.Compose(
    [
        transforms.Resize(64),
        transforms.CenterCrop(64),
        transforms.ToTensor()
    ]
)

img_names = os.listdir(rootdir)
filenames = [os.path.join(rootdir, f) for f in img_names]

totalsize = sum([os.stat(f).st_size for f in filenames])
print(totalsize / 1e6)

to_batched_npy(transform, rootdir, savedir, 100)


c_names = os.listdir(savedir)
filenames = [os.path.join(savedir, f) for f in c_names]

totalsize = sum([os.stat(f).st_size for f in filenames])
print(totalsize / 1e6)


zipped_imgs = gzip.GzipFile(
   os.path.join(savedir, f"batch100.npy.gz"), 
   "r"
)
imgs = np.load(zipped_imgs)
zipped_imgs.close()

