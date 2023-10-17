import pyaws

source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
save_dir = 's3://celeba-demo-bucket'
profile = "nick"
notify_after = 2

pyaws.copy_dir(
    source_dir,
    save_dir,
    profile,
    notify_after
)

dir = '/home/nicholas/Datasets/CelebA/ret'
pyaws.copy_dir(
    save_dir,
    dir,
    profile,
    notify_after
)

pyaws.sync_dir(
    save_dir,
    dir,
    profile,
    notify_after=1
)
