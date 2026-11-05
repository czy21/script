```shell
# https://velero.io/docs/v1.19/resource-filtering/
velero restore create <restore-name> --include-namespaces stable --from-backup <backup-name>
```