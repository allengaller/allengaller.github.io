# etcd deployment

[guide](http://play.etcd.io/install)

## system requirements

The etcd performance benchmarks run etcd on 8 vCPU, 16GB RAM, 50GB SSD GCE instances, but any relatively modern machine with low latency storage and a few gigabytes of memory should suffice for most use cases. Applications with large v2 data stores will require more memory than a large v3 data store since data is kept in anonymous memory instead of memory mapped from a file. 

## download the pre-built binary

The easiest way to get etcd is to use one of the pre-built release binaries which are available for OSX, Linux, Windows, appc, and Docker. Instructions for using these binaries are on the [GitHub releases page](https://github.com/etcd-io/etcd/releases/).

## installation

linux
```
ETCD_VER=v3.3.13

# choose either URL
GOOGLE_URL=https://storage.googleapis.com/etcd
GITHUB_URL=https://github.com/etcd-io/etcd/releases/download
DOWNLOAD_URL=${GOOGLE_URL}

rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
rm -rf /tmp/etcd-download-test && mkdir -p /tmp/etcd-download-test

curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz
tar xzvf /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz -C /tmp/etcd-download-test --strip-components=1
rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz

/tmp/etcd-download-test/etcd --version
ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl version
```

action
```
[root@k8s-ttt-main-1 ~]# vim etcd.install.sh
[root@k8s-ttt-main-1 ~]# chmod +x etcd.install.sh
```

testing
```
# start a local etcd server
/tmp/etcd-download-test/etcd

# write,read to etcd
ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put foo bar
ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get foo
```