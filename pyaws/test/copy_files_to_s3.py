import pyaws

source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
bucket_name = 'celeba-demo-bucket'
profile = "nick"
notify_after = 2

pyaws.copy_dir_to_s3(
    source_dir,
    bucket_name,
    profile,
    notify_after
)

pyaws.sync_dir_to_s3(
    source_dir,
    bucket_name,
    profile,
    notify_after=0
)
