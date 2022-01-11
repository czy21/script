## init
```shell
sudo dpkg-reconfigure dash # select no sh => bash
```
# manual cp and compress
```bash
storage_dir=/srv/dev-disk-by-id-scsi-1ATA_ST4000NM000A-2HZ100_WS213MF7-part1/storage;\
module_name=docker-data;\
tar -czvf ${storage_dir}/backup/${module_name}-$(date +%Y%m%d-%H%M).tar.gz -C ${storage_dir} ${module_name}
```