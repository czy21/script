# dockerfile

# docker-compose
```yaml
version: "3.9"
services:
  etcd-1-1:
    image: coreos/etcd:v3.5.5 # quay.io/coreos/etcd
    container_name: etcd-1-1
    hostname: etcd-1-1
    privileged: true
    user: root
    expose: []
    ports:
      - "2381:2381"
      - "2382:2382"
    volumes:
      - /volume1/storage/docker-data/etcd-1/data/1/:/data/
    command: etcd
      --data-dir=/data/etcd --name etcd-1-1
      --advertise-client-urls http://<ip>:2381 --listen-client-urls http://0.0.0.0:2381
      --initial-advertise-peer-urls http://<ip>:2382 --listen-peer-urls http://0.0.0.0:2382
      --initial-cluster etcd-1-1=http://<ip>:2382,etcd-1-2=http://<ip>:2384,etcd-1-3=http://<ip>:2386
      --initial-cluster-state new --initial-cluster-token etcd-1
    restart: always
  etcd-1-2:
    image: coreos/etcd:v3.5.5 # quay.io/coreos/etcd
    container_name: etcd-1-2
    hostname: etcd-1-2
    privileged: true
    user: root
    expose: []
    ports:
      - "2383:2383"
      - "2384:2384"
    volumes:
      - /volume1/storage/docker-data/etcd-1/data/2/:/data/
    command: etcd
      --data-dir=/data/etcd --name etcd-1-2
      --advertise-client-urls http://<ip>:2383 --listen-client-urls http://0.0.0.0:2383
      --initial-advertise-peer-urls http://<ip>:2384 --listen-peer-urls http://0.0.0.0:2384
      --initial-cluster etcd-1-1=http://<ip>:2382,etcd-1-2=http://<ip>:2384,etcd-1-3=http://<ip>:2386
      --initial-cluster-state new --initial-cluster-token etcd-1
    restart: always
  etcd-1-3:
    image: coreos/etcd:v3.5.5 # quay.io/coreos/etcd
    container_name: etcd-1-3
    hostname: etcd-1-3
    privileged: true
    user: root
    expose: []
    ports:
      - "2385:2385"
      - "2386:2386"
    volumes:
      - /volume1/storage/docker-data/etcd-1/data/3/:/data/
    command: etcd
      --data-dir=/data/etcd --name etcd-1-3
      --advertise-client-urls http://<ip>:2385 --listen-client-urls http://0.0.0.0:2385
      --initial-advertise-peer-urls http://<ip>:2386 --listen-peer-urls http://0.0.0.0:2386
      --initial-cluster etcd-1-1=http://<ip>:2382,etcd-1-2=http://<ip>:2384,etcd-1-3=http://<ip>:2386
      --initial-cluster-state new --initial-cluster-token etcd-1
    restart: always
```