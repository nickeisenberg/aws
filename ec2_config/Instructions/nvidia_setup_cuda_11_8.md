1. Previous steps include...

    - 1.1. Generating an access key

    - 1.2. Setting up `aws configure --profile`

    - 1.3. Generating a key pair

    - 1.4. Making a security group that allows for sufficient inbound and outbount privileges. This 
    includes SSH, HTTP, HTTPS and IMCP.

2. Create the ec2 instance

3. Get the public IP address for the 

4. Apon first SSH into the instance, update apt and upgrade by running `sudo apt update` and
`sudo apt upgrade`. 

5. This will require a reboot to reset the headers. Do the followin to reboot:

    - 5.1. Stop the SSH connection

    - 5.2. Run the following command in your local terminal. (Make sure you already have done
    - `aws configure --profile`)
    - 
        ```
        aws ec2 reboot-instances \
                --region <region_name> \
                --instance-ids <instance_id> \
                --profile <profile_name>
        ```

    - 5.3. Wait like 30 seconds and SSH back into the instance.

6. Next run `sudo apt install neofetch`. This is just a nice little too to have.

7. Run `neofetch` and you should see an nvidia GPU. If not, then run `lspci | grep -i nvidia`.
If this returns nothing, then the instance has no nvidia gpu.

8. Next we will install the GPU drivers. The steps are extremely important to follow exactly.

9. Run `sudo apt install nvidia-driver-535`

10. Reboot the instance by doing the same thing we did above.

11. SSH back into the instance and run `nvidia-smi`. If this works then continue. If there is
an error message then maybe you messed up something from above. Ignore the CUDA version
that is illustrated in the `nvidia-smi` output. THIS IS NOT THE CUDA VERSION INSTALLED, but
the highest CUDA version that is approved. The driver is backward compatible so older CUDA
version will still work.

12. Next we need to install the cuda toolkit. We will use 11.8 as this is the most widely
accepted version as of now.

13. Run `mkdir -p ~/Software/cuda` and `cd` into this directory with `cd ~/Software/cuda`.

14. In this directory, run `wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run`

15. Next install it with `sudo sh cuda_11.8.0_520.61.05_linux.run`. The install hangs, so
be patient.

16. There is going to be a warning message telling you to abort. Ignore it and choose that you
want to continue. After continuing, say that you accept.

17. NEXT MAKE SURE THAT YOU UNSELECT THE DRIVER!!!!!! You can use the arrow keys to move around
    and use the enter key to select or de-delect. ONLY AFTER DE-SELECTING THE DRIVER, use the arrows
    to move the install icon and hit enter. The install hangs again, so be patient. The output of a
    successful install is the following
    ```
    ===========
    = Summary =
    ===========
    
    Driver:   Not Selected
    Toolkit:  Installed in /usr/local/cuda-11.8/
    
    Please make sure that
     -   PATH includes /usr/local/cuda-11.8/bin
     -   LD_LIBRARY_PATH includes /usr/local/cuda-11.8/lib64, or, add /usr/local/cuda-11.8/lib64 to /etc/ld.so.conf and run ldconfig as root
    
    To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-11.8/bin
    ***WARNING: Incomplete installation! This installation did not install the CUDA Driver. A driver of version at least 520.00 is required for CUDA 11.8 functionality to work.
    To install the driver using this installer, run the following command, replacing <CudaInstaller> with the name of this run file:
        sudo <CudaInstaller>.run --silent --driver
    
    Logfile is /var/log/cuda-installer.log
    ```


18. Edit the `~/.bashrc` (or `~/.bash_profile` if you use that) and add the follwing lines
    anywhere in these files:

    ```
    export PATH="/usr/local/cuda/bin:$PATH"
    export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"
    ```

    Considering that there are two options here, the `.bashrc` or `.bash_profile` option, 
    I recommend doing the following:
    
    - 18.1. Create the directory `~/Dotfiles` with `mkdir ~/Dotfiles`.
    
    - 18.2. `cd` into this directory and run `mkdir ~/Dotfile/.config`. This `.config`
    is used for any user configuration later on
    
    - 18.3. Now create the `.bash_profile` file within `~/Dotfiles` by running 
    
    - `touch ~/Dotfiles/.bash_profile`
    
    - 18.4. Symlink this file to the place where linux actually looks by running 
    `ln -s ~/Dotfiles/.bash_profile ~/.bash_profile`.
    
    - 18.5. With this symlink, you can either edit `~/.bash_profile` or `~/Dotfiles/.bash_profile`
    and the changes will occur in both spots.
    
    - 18.6. Now open the file with `vi ~/Dotfiles/.bash_profile` or `vi ~/.bash_profile` and 
    add the following lines
        ```
        source ~/.bashrc
        export PATH="/usr/local/cuda/bin:$PATH"
        export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"
        ```
    
    - 18.7. The reason why I like this method, is becuase you can now source control all
    of your config files with `git`. You can push this whole `~/Dotfiles` folder to github
    and now all of you config files are tracked so whenever you start up a new EC2 instance,
    you can just reload the config files and save time.
    
    - 18.8. If you took my recomendation then skip to step 20. Otherwise, go to step 19.

19. Now source with file with `source ~/.bashrc` (or `source ~/.bash_profile`)

20. Run `echo "/usr/local/cuda/lib64" | sudo tee -a /etc/ld.so.conf' and also 
`sudo ldconfig`

21. To check if thinks worked, you can run `ldconfig -p | grep cuda`. A bunch of stuff
should appear.

22. Lastly, run `cat /usr/local/cuda/version.json | grep version -B 2`. The top of this
output should say something like this:
```
"cuda" : {
      "name" : "CUDA SDK",
      "version" : "11.8.20220929"
   },
```

23. If you run `nvcc --version` then you should get:
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Sep_21_10:33:58_PDT_2022
Cuda compilation tools, release 11.8, V11.8.89
Build cuda_11.8.r11.8/compiler.31833905_0
```

24. One last check will be to see if cupy, numba and pytorch can access the GPU.
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
```

25. Once the gpu is set up, `aws configure --profile` should then be set up within the EC2 instance.

26. At this point, I believe any further configuration will just be personal taste.
