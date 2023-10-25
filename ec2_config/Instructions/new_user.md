* It is helpful to first direct `visudo` to use vi and not nano. To do this, run
`sudo update-alternatives --config editor` and chose the `vim basic` option.

* Steps to add a new user
1. `sudo adduser <new_user_name>`

2. There are a couple ways to grant privileges.

    - 2.1. You can use `usermod -aG <groupname> <new_user_name>` to add 
    the new user to the group `<groupname>`. To check the groups you can run 
    `groups ubuntu` to see all the groups all the groups
    that the main user, which is `ubuntu` on ubunut ec2 instances, belongs too.

    - 2.2 You can edit `/etc/sudoers`. To do this, run `visudo /etc/sudoers` and 
    add the line `<new_user_name> ALL=(ALL:ALL) ALL` underneath the line 
    `root ALL=(ALL:ALL) ALL`.

3. To check to see if all works, log in to the this newle added user with 
`su -l <new_user_name>` and see if you can use `sudo`. Try `sudo vi tempfile.txt`.
If this works then all is well.

4. To delete a user...
    
    - 4.1 To delete the user but keep all of their files, you can run 
    `sudo deluser <user_name>`.

    - 4.2 To delete the user and all the config files, run 
    `sudo deluser --remove-home <user_name>`

    -4.3 Remove all prvileges that were added to this user in `/etc/sudoers` by using 
    `visudo`


 
