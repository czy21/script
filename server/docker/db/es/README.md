## Other
```shell
# switch root
echo "vm.max_map_count=262144" >> /etc/sysctl.conf
sudo sysctl -p

# fix warning Missing replica shards
PUT _settings
{
  "number_of_replicas": 0
}
```