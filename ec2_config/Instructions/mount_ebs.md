1. Run `lsblk` to find the name of the volume that was added from the aws consol.

2. Format the volume with `sudo mkfs -t ext4 /dev/xvdf`

3. Create the folder inside `dev` that will be used to mount the volume. For 
example `sudo mkdir /data`

4. Mount the volume to the folder you made by running 
`sudo mount /dev/<name_of_volume> /data`

5. Running `df -H` should now show the added volume.
