import os
import shutil



def to_batched_zips(sourcedir, savedir, ims_per_batch):

    filenames = [os.path.join(sourcedir, f) for f in os.listdir(sourcedir)]

    temp = os.path.join(savedir, "temp")
    os.makedirs(temp)

    batch_num = 0
    for i, f in enumerate(filenames):
        shutil.copy(f, temp)

        if (i + 1) % ims_per_batch == 0:
    
            batch_num += 1
            arxiv = os.path.join(savedir, f"batch{batch_num}")
            shutil.make_archive(arxiv, "zip", temp)

            shutil.rmtree(temp)
            os.makedirs(temp)

            print(f"BATCH {batch_num} COMPLETE")

    shutil.rmtree(temp)
    print("Process Complete")

    return None


savedir = "/home/nicholas/Datasets/CelebA/batched"
sourcedir = "/home/nicholas/Datasets/CelebA/img_align_celeba_10000"

to_batched_zips(
    sourcedir=sourcedir,
    savedir=savedir,
    ims_per_batch=1000
)
