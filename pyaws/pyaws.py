import subprocess

def copy_dir(
    source_dir, 
    save_dir,
    profile,
    notify_after=0
    ):

    """
    A python function that calls a bash function that applies 
    aws s3 cp --recurisve on a whole local directory. According to the internet
    aws s3 cp is faster aws s3 sync and I believe both of these are faster than
    using boto3 functions directly to move files from local to s3.

    Parameters
    ----------
    source_dir: str
        The full file path to the local dir containing the files that need to be
        moved.
    save_dir: str
        Full path of the dir being saved to.
    profile: str
        The name of the profile that is configured with aws configure
    notify_after: str default 0
        This will return a status message to the python interpreter after each
        "notify_after" file shave been uploaded. 0 will silent all notifiations.

    Returns
    -------
    None
    
    Example
    -------

    source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
    save_dir = 's3://celeba-demo-bucket'
    profile = "nick"
    notify_after = 2

    pyaws.copy_dir_to_s3(
        source_dir,
        save_dir,
        profile,
        notify_after
    )
    """

    # path_to_bash = "/home/nicholas/GitRepos/aws/pyaws/scripts"
    path_to_bash = "./scripts"
    path_to_bash += "/copy_dir.sh"

    try:
        # Call the Bash script with specified parameters
        with subprocess.Popen(
            [
                path_to_bash, 
                "--source-dir", 
                source_dir, 
                "--save-dir", 
                save_dir, 
                "--profile", 
                profile, 
                "--notify-after", 
                str(notify_after)
            ],
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        ) as p:
            for line in p.stdout:
                print(line, end='')


    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")
    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None


def sync_dir(
    source_dir, 
    # bucket_name,
    save_dir,
    profile,
    notify_after=0
    ):

    """
    A python function that calls a bash function that applies 
    aws s3 sync on a whole local directory. According to the internet
    aws s3 cp is faster aws s3 sync and I believe both of these are faster than
    using boto3 functions directly to move files from local to s3. However, 
    sync seems to be just as fast as cp. I think sync is mainly for when you 
    dont want to overwrite files already in a bucket. Sync will not copy the 
    file over if it already exists so if you are moving alot of files then sync 
    may take some extra time making sure that it does not move files over that 
    are already there. I could be wrng about this.

    Parameters
    ----------
    source_dir: str
        The full file path to the local dir containing the files that need to be
        moved to s3.
    bucket_name: str
        Just the name of the s3 bucket. In other words, <bucket_name> and not
        s3://<bucket_name>.
        
    profile: str
        The name of the profile that is configured with aws configure
    notify_after: str default 0
        This will return a status message to the python interpreter after each
        "notify_after" file shave been uploaded. 0 will silent all notifiations.

    Returns
    -------
    None


    Example
    -------
    source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
    save_dir = 's3://celeba-demo-bucket'
    profile = "nick"
    notify_after = 2

    pyaws.copy_dir_to_s3(
        source_dir,
        save_dir,
        profile,
        notify_after
    )
    """
    
    # path_to_bash = "/home/nicholas/GitRepos/aws/pyaws/scripts"
    path_to_bash = "./scripts"
    path_to_bash += "/sync_dir.sh"

    try:
        # Call the Bash script with specified parameters
        with subprocess.Popen(
            [
                path_to_bash, 
                "--source-dir", 
                source_dir, 
                # "--bucket-name", 
                # bucket_name, 
                "--save-dir", 
                save_dir, 
                "--profile", 
                profile, 
                "--notify-after", 
                str(notify_after)
            ],
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        ) as p:
            for line in p.stdout:
                print(line, end='')


    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")
    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")

    return None
