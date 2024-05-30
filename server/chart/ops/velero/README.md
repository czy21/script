```shell
# https://velero.io/docs/v1.8/resource-filtering/
velero restore create <restore-name> --include-namespaces stable --from-backup <backup-name>
```