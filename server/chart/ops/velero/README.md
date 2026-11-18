# Detail
```shell
velero -n ops backup get
velero -n ops backup describe <backup-name> --details
```
# Backup
```shell
velero -n ops backup create --from-schedule velero-daily --wait
```
# Restore
```shell
velero -n ops restore create --from-backup <backup-name> --wait
```