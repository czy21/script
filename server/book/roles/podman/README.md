## Guide
```text
https://github.com/containers/podman/blob/main/troubleshooting.md
```
## Storage
```shell
cat ~/.config/containers/storage.conf
[storage]
  driver = "overlay"
  runroot = "/run/user/1000"
  graphroot = "/execdir/myuser/storage"
```