```shell
sudo hostnamectl set-hostname --static [hostname]
# ubuntu enable remote desktop
sudo apt install xrdp

# pull
rsync --archive --delete --progress --verbose rsync://<username>@<host>:<remote_path> <local_path>
```
# Mount
```shell
# get device name
fdisk -l
# get device uuid
blkid /dev/sdb1
# disk in /etc/fstab
/dev/disk/by-uuid/[uuid] /volume1 ext4 defaults 0 0

# show nfs
showmount -e [host]
# nfs in /etc/fstab
[host]:/volume1/ubuntu /volume1 nfs defaults 0 0

# nfs command line
sudo mount -t nfs <nfs_server>:/<nfs_path> /<local_path>

# smb in /etc/fstab
//<host>/public/ubun12   /volume2   cifs   user=<username>,pass=<password>,gid=1000,uid=1000    0 0

# smb command line
sudo mount -t cifs //<smb_server>/<smb_path> /<local_path> -o "user=<username>,password=<password>,gid=1000,uid=1000"
```