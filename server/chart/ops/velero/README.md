```shell
# https://velero.io/docs/v1.8/resource-filtering/
velero restore create <restore-name> --include-resources deployments,configmaps --from-backup <backup-name>
```