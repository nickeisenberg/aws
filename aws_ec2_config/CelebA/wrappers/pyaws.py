import subprocess

DIR = "/home/nicholas/GitRepos/learn_aws/aws_ec2_config/CelebA"


def push_folder_to_s3(
    rootdir,
    bucketdir,
    profile
    ):
    bash = [
        f"{DIR}/wrappers/scripts/sync_wrapper.sh",
        "--rootdir",
        f"{rootdir}",
        "--bucketdir",
        f"{bucketdir}",
        "--profile",
        f"{profile}"
    ]
    subprocess.call(bash)


def copy_folder_to_s3(
    source_dir,
    bucket_name,
    notify_after
    ):
    bash = [
        f"{DIR}/wrappers/scripts/cp_dir_to_s3.sh",
        "--source-dir",
        f"{source_dir}",
        "--bucket-name",
        f"{bucket_name}",
        "--notify-after",
        f"{notify_after}"
    ]
    subprocess.call(bash)


def copy_dir_to_s3(
    source_dir, 
    bucket_name,
    profile,
    notify_after=0
    ):

    bash_script_path = f"{DIR}/wrappers/scripts/cp_dir_to_s3.sh"

    try:
        # Call the Bash script with specified parameters
        subprocess.check_call(
            [
                # "bash", 
                bash_script_path, 
                "--source-dir", 
                source_dir, 
                "--bucket-name", 
                bucket_name, 
                "--profile", 
                profile, 
                "--notify-after", 
                str(notify_after)
            ]
        )
        print("Files copied to S3 successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")
    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")



def copy_dir_to_s3_2(
    source_dir, 
    bucket_name, 
    profile, 
    notify_after=0
    ):
    # Specify the path to the Bash script
    bash_script_path = f"{DIR}/wrappers/scripts/cp_dir_to_s3.sh"

    try:
        # Call the Bash script with specified parameters and capture its output
        process = subprocess.Popen(
            [
                "bash", 
                bash_script_path, 
                "--source-dir", 
                source_dir, 
                "--bucket-name", 
                bucket_name, 
                "--profile", 
                profile, 
                "--notify-after", 
                str(notify_after)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read and print the output line by line in real-time
        for line in process.stdout:
            print(line, end='')

        # Wait for the process to finish
        process.wait()

        if process.returncode == 0:
            print("Files copied to S3 successfully.")
        else:
            print("Failed to copy files to S3.")
    except subprocess.CalledProcessError as e:
        print(f"Error calling the Bash script: {e}")
    except FileNotFoundError as e:
        print(f"Bash script not found: {e}")








