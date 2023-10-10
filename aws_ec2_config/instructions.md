* Previous steps include...
1. Generating an access key
2. Setting up `aws configure --profile`
3. Generating a key pair
4. Making a security group that allows for sufficient inbound and outbount privileges. This 
includes SSH, HTTP, HTTPS and IMCP.

* Use `spot_config.py` to create the EC2 spot instance. The config for this spot instance
can be eaisly generated using the aws consol. For example, go to the EC2 tab in the consol
and on the left navigation pane, choose `Spot Requests`. There is a `configure json` option right
by the launch request button.

* Get the public IP address for the 

* Apon fir SSH into the instance, update apt and upgrade by running:

`sudo apt update`
`sudo apt upgrade`

* This will require a reboot to reset the headers. Do the followin to reboot:
1) Stop the SSH connection
2) Run the following command in your local terminal. (Make sure you already have done
`aws configure --profile`)
```
aws ec2 reboot-instances \
        --region <region_name> \
        --instance-ids <instance_id> \
        --profile <profile_name>
```
3) Wait like 30 seconds and SSH back into the instance.

* Next run `sudo apt install neofetch`. This is just a nice little too to have.

* Run `neofetch` and you should see an nvidia GPU. If not, then run `lspci | grep -i nvidia`.
If this returns nothing, then the instance has no nvidia gpu.

* Next we will install the GPU drivers. The steps are extremely important to follow exactly.
1. Run `sudo apt install nvidia-driver-535`
2. Reboot the instance by doing the same thing we did above.
3. SSH back into the instance and run `nvidia-smi`. If this works then continue. If there is
an error message then maybe you messed up something from above. Ignore the CUDA version
that is illustrated in the `nvidia-smi` output. THIS IS NOT THE CUDA VERSION INSTALLED, but
the highest CUDA version that is approved. The driver is backward compatible so older CUDA
version will still work.
4. Next we need to install the cuda toolkit. We will use 11.8 as this is the most widely
accepted version as of now.
5. Run `mkdir -p ~/Software/cuda` and `cd` into this directory with `cd ~/Software/cuda`.
6. In this directory, run `wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run`
7. Next install it with `sudo sh cuda_11.8.0_520.61.05_linux.run`. The install hangs, so
be patient.
8. There is going to be a warning message telling you to abort. Ignore it and choose that you
want to continue. After continuing, say that you accept.
9. NEXT MAKE SURE THAT YOU UNSELECT THE DRIVER!!!!!! You can use the arrow keys to move around
and use the enter key to select or de-delect. ONLY AFTER DE-SELECTING THE DRIVER, use the arrows
to move the install icon and hit enter. The install hangs again, so be patient.
10. Edit the `~/.bashrc` (or `~/.bash_profile` if you use that) and add the follwing lines
anywhere in these files:
```
export PATH="/usr/local/cuda/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"
```
Considering that there are two options here, the `.bashrc` or `.bash_profile` option, 
I recommend doing the following:
    10.1. Create the directory `~/Dotfile` with `mkdir ~/Dotfiles`.
    10.2. `cd` into this directory and run `mkdir ~/Dotfile/.config`. This `.config`
    is used for any user configuration later on
    10.3. Now create the `.bash_profile` file within `~/Dotfile` by running 
    `touch ~/Dotfiles/.bash_profile`
    10.4. Symlink this file to the place where linux actually looks by running 
    `ln -s ~/Dotfiles/.bash_profile ~/.bash_profile`.
    10.5. With this symlink, you can either edit `~/.bash_profile` or `~/Dotfiles/.bash_profile`
    and the changes will occur in both spots.
    10.6. Now open the file with `vi ~/Dotfiles/.bash_profile` or `vi ~/.bash_profile` and 
    add the following lines
    ```
    source ~/.bashrc
    export PATH="/usr/local/cuda/bin:$PATH"
    export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"
    ```
    10.7. The reason why I like this method, is becuase you can now source control all
    of your config files with `git`. You can push this whole `~/Dotfiles` folder to github
    and now all of you config files are tracked so whenever you start up a new EC2 instance,
    you can just reload the config files and save time.
    10.8. If you took my recomendation then skip to step 12. Otherwise, go to step 11.
11. Now source with file with `source ~/.bashrc` (or `source ~/.bash_profile`)
12. Run the following:
```
echo "/usr/local/cuda/lib64" | sudo tee -a /etc/ld.so.conf
sudo ldconfig
```
13. To check if thinks worked, you can run `ldconfig -p | grep cuda`. A bunch of stuff
should appear.

14. Lastly, run `cat /usr/local/cuda/version.json | grep version -B 2`. The top of this
output should say something like this:
```
"cuda" : {
      "name" : "CUDA SDK",
      "version" : "11.8.20220929"
   },
```
15. If you run `nvcc --version` then you should get:
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Sep_21_10:33:58_PDT_2022
Cuda compilation tools, release 11.8, V11.8.89
Build cuda_11.8.r11.8/compiler.31833905_0
```
16. One last check will be to see if cupy, numba and pytorch can access the GPU.
To do this, first run `sudo apt install python3.10-venv`. Then run `mkdir -p ~/Software/venv`.
Then cd into this directory with `cd ~/Software/venv` and run `python3 -m venv test_cuda`.
Lastly, run `source ~/Software/venv/test_cuda/bin/activate` to activate the virtual
enviornment. Now install pytorch, cupy and numba with the following.
```
pip install cupy-cuda11x
pip install numba
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
Lastly, create a python script and put the following into it and run it. If the script
returns all the affirmative responses then you are all good.

```
"""
A simple test to see if the GPU is functional
"""

try:
    import cupy
    print("cupy can be imported")
except:
    print("cupy could not be imported")

from numba.cuda import is_available as numba_works
from torch.cuda import is_available as torch_works

if numba_works():
    print("Numba cuda works")
else:
    print("Numba does not work")

if torch_works():
    print("torch cuda works")
else:
    print("torch does not work")
`

* One the gpu is set up, `aws configure --profile` should then be set up within the EC2 instance.

* At this point, I believe any further configuration will just be personal taste.
