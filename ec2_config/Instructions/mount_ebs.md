1. Run `lsblk` to find the name of the volume that was added from the aws consol.

3. Format the volume with `sudo mkfs -t ext4 /dev/xvdf`

3. Create the folder inside `dev` that will be used to mount the volume. For 
example `sudo mkdir /data`

4. Mount the volume to the folder you made by running 
`sudo mount /dev/<name_of_volume> /data`

5. Running `df -H` should now show the added volume.

6. Run `sudo chown <your username>:<your usergroup> -R <path to volume>` to remove
the sudo need for it. This way you can move files to the volume using the aws cli
