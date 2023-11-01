"""
Use this script for some initial setup of the ec2 instnace.
Use pyaws.transfer.scp to move the files over
"""

from pyaws.transfer import scp

save_path = "/home/ubuntu/Dotfiles/scripts"
user = "ubuntu"
ip = "18.144.88.213"

sources = [
    "/home/nicholas/Dotfiles/scripts/localpip.sh",
    "/home/nicholas/Dotfiles/scripts/venv.sh",
]

for source in sources:
    scp(source, save_path, user, ip)
