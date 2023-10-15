import pyaws

source_dir = '/home/nicholas/Datasets/CelebA/img_64_10'
bucket_name = 'celeba-demo-bucket'
notify_after = 2

pyaws.copy_dir_to_s3(
    source_dir=source_dir,
    bucket_name=bucket_name,
    profile='nick',
    notify_after=notify_after
)

import subprocess

DIR = "/home/nicholas/GitRepos/learn_aws/aws_ec2_config/CelebA"
bash_script_path = f"{DIR}/wrappers/scripts/cp_dir_to_s3.sh"

bash_script_path += f" --bucket-name {bucket_name}"
bash_script_path += f" --source-dir {source_dir}"
bash_script_path += f" --profile nick"
bash_script_path += f" --notify-after {notify_after}"

# Call the Bash script with specified parameters
f = open(bash_script_path, "rb")

x = [
    "bash", 
    bash_script_path, 
    "--source-dir", 
    source_dir, 
    "--bucket-name", 
    bucket_name, 
    "--profile", 
    "nick", 
    "--notify-after", 
    str(notify_after)
]

p = subprocess.Popen(
    "sh",
    shell=True,
    stdin=f,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding="utf-8"
)

f.close()

while True:
    c = p.stdout.read(1)
    if not c:
        break
    print(c, end='')
print()
