# windows python c++ build tool install
## install vs2022
## selected windows sdk and

# create venv
```shell
python3 -m venv .python3
```
# pip conf https://pip.pypa.io/en/stable/topics/configuration/
```ini
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```
```ini
[global]
index-url = http://nexus.czy21-internal.com/repository/pypi-proxy/simple/
[install]
trusted-host=nexus.czy21-internal.com
```

```bash
wget -O - https://bootstrap.pypa.io/get-pip.py | python3
```