To be able to render matplotlib plot generated from the ec2 instance on the 
local machine, you need to enable X11 forwarding and install tkinter on the 
remote instance.

1. First ssh into the ec2 instance and open up `/etc/ssh/ssh_config` and 
uncomment the line that says `ForwardX11 no` and replace `no` with `yes`.
save the file. Note that this file must be editted with `sudo vi` as this
is a proftected file.

2. Terminate the connection and reboot the ec2 instance with the line:
    ```
    aws ec2 reboot-instances \
            --region <region_name> \
            --instance-ids <instance_id> \
            --profile <profile_name>
    ```

aws ec2 reboot-instances \
        --region us-west-1 \
        --instance-ids i-05cbf3049d9af51e4 \
        --profile nick

3. Now, ssh back in the instance but make sure you add the `-X` tag into your
ssh command. For example, `ssh -X -i <key-pair.pem> ubuntu@<ip-addr>`

4. Make sure `tkinter` is installed. Do this with `sudo apt install python3-tk`

5. Now, each time you want to use `matplotlib`, make sure you import it as follows:
    ```
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    ```

6. Now all `matplotlib` plot generated on the ec2 instance should render locally 
on your computer.
