import subprocess

def push_folder_to_s3(
    rootdir,
    bucketdir,
    profile
    ):
    bash = [
        "/home/nicholas/GitRepos/learn_aws/boto3/celeba_ex/wrappers/./sync_wrapper.sh",
        "--rootdir",
        f"{rootdir}",
        "--bucketdir",
        f"{bucketdir}",
        "--profile",
        f"{profile}"
    ]
    subprocess.call(bash)
