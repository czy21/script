## Docker Build
```shell
-p param_registry_targets=github,dockerhub  # 推送目标
```

## omv: /volume2 => es,minio,ch,ndisk

## Use
```shell
# nas
bash main.sh <user@host> install -p param_cluster_name=nas
# dsm
bash main.sh <user@host> install -p param_cluster_name=dsm --env-active syno
```