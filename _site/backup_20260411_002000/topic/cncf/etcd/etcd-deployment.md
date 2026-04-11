# etcd deployment

[guide](http://play.etcd.io/install)

## system requirements

* The etcd performance benchmarks run etcd on 8 vCPU, 16GB RAM, 50GB SSD GCE instances, but any relatively modern machine with low latency storage and a few gigabytes of memory should suffice for most use cases. Applications with large v2 data stores will require more memory than a large v3 data store since data is kept in anonymous memory instead of memory mapped from a file. 

## download the pre-built binary

* The easiest way to get etcd is to use one of the pre-built release binaries which are available for OSX, Linux, Windows, appc, and Docker. Instructions for using these binaries are on the [GitHub releases page](https://github.com/etcd-io/etcd/releases/).

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

version check
```
[root@k8s-ttt-us-1 ~]# /tmp/etcd-download-test/etcd --version
etcd Version: 3.3.13
Git SHA: 98d3084
Go Version: go1.10.8
Go OS/Arch: linux/amd64
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl version
etcdctl version: 3.3.13
API version: 3.3
```

testing
```
# start a local etcd server
/tmp/etcd-download-test/etcd

# write,read to etcd
ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put foo bar
ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get foo
```

put get
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put foo bar
OK
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get foo
foo
bar
```

files
```
[root@k8s-ttt-us-1 etcd-download-test]# ll
总用量 29776
drwxr-xr-x 10 1000 1000     4096 5月   3 01:55 Documentation
-rwxr-xr-x  1 1000 1000 16927136 5月   3 01:55 etcd
-rwxr-xr-x  1 1000 1000 13498880 5月   3 01:55 etcdctl
-rw-r--r--  1 1000 1000    38864 5月   3 01:55 README-etcdctl.md
-rw-r--r--  1 1000 1000     7262 5月   3 01:55 README.md
-rw-r--r--  1 1000 1000     7855 5月   3 01:55 READMEv2-etcdctl.md
```

## demo

put get
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put foo bar
OK
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get foo
foo
bar
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 --write-out="json" get foo
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":2,"raft_term":2},"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":2,"version":1,"value":"YmFy"}],"count":1}
```

get by prefix
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put web1 value1
OK
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put web2 value2
OK
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put web3 value3
OK
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get web --prefix
web1
value1
web2
value2
web3
value3
```

del
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 del web1
1
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get web --prefix
web2
value2
web3
value3
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 del web --prefix
2
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get web --prefix
[root@k8s-ttt-us-1 ~]#
```

transactional write
txn to wrap multiple requests into one transaction:
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 txn --interactive
compares:
value("user1") = "bad"

success requests (get, put, del):
del user1

failure requests (get, put, del):
put user1 good

SUCCESS

1
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get user1
[root@k8s-ttt-us-1 ~]#
```

watch
watch to get notified of future changes:
vm 1
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 watch u --prefix
PUT
user123
123
```
vm 2
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put user123 123
OK
```

lease
lease to write with TTL:
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 lease grant 300
lease 694d6c7ee25f0717 granted with TTL(300s)
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 put sample value --lease=694d6c7ee25f0717
OK
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get sample
sample
value
```
5min later
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 get sample
[root@k8s-ttt-us-1 ~]#
```

distributed locks
lock for distributed lock:
vm1
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 lock mutex1
mutex1/694d6c7f37654404

```
vm2
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 lock mutex1

```

elections
elect for leader election:
vm1
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 elect one p1
one/694d6c7f396a7110
p1
```
vm2(after kill p1)
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 elect one p2
one/694d6c7f396a711a
p2
```

cluster status
specify the initial cluster configuration for each machine:
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 endpoint status --write-out=table
+----------------+------------------+---------+---------+-----------+-----------+------------+
|    ENDPOINT    |        ID        | VERSION | DB SIZE | IS LEADER | RAFT TERM | RAFT INDEX |
+----------------+------------------+---------+---------+-----------+-----------+------------+
| localhost:2379 | 8e9e05c52164694d |  3.3.13 |   25 kB |      true |         4 |         61 |
+----------------+------------------+---------+---------+-----------+-----------+------------+
```

health
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 endpoint health
localhost:2379 is healthy: successfully committed proposal: took = 571.607µs
```

snapshot
snapshot to save point-in-time snapshot of etcd database:
```
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 snapshot save my.db
Snapshot saved at my.db
[root@k8s-ttt-us-1 ~]# ETCDCTL_API=3 /tmp/etcd-download-test/etcdctl --endpoints=localhost:2379 --write-out=table snapshot status my.db
+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| dab7b5a |       32 |         36 |      25 kB |
+---------+----------+------------+------------+
```

migrate
migrate to transform etcd v2 to v3 data:
```
# write key in etcd version 2 store
export ETCDCTL_API=2
etcdctl --endpoints=http://$ENDPOINT set foo bar

# read key in etcd v2
etcdctl --endpoints=$ENDPOINTS --output="json" get foo

# stop etcd node to migrate, one by one

# migrate v2 data
export ETCDCTL_API=3
etcdctl --endpoints=$ENDPOINT migrate --data-dir="default.etcd" --wal-dir="default.etcd/member/wal"

# restart etcd node after migrate, one by one

# confirm that the key got migrated
etcdctl --endpoints=$ENDPOINTS get /foo
```

member
member to add,remove,update membership:
```
# For each machine
TOKEN=my-etcd-token-1
CLUSTER_STATE=new
NAME_1=etcd-node-1
NAME_2=etcd-node-2
NAME_3=etcd-node-3
HOST_1=10.240.0.13
HOST_2=10.240.0.14
HOST_3=10.240.0.15
CLUSTER=${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_3}=http://${HOST_3}:2380

# For node 1
THIS_NAME=${NAME_1}
THIS_IP=${HOST_1}
etcd --data-dir=data.etcd --name ${THIS_NAME} \
	--initial-advertise-peer-urls http://${THIS_IP}:2380 \
	--listen-peer-urls http://${THIS_IP}:2380 \
	--advertise-client-urls http://${THIS_IP}:2379 \
	--listen-client-urls http://${THIS_IP}:2379 \
	--initial-cluster ${CLUSTER} \
	--initial-cluster-state ${CLUSTER_STATE} \
	--initial-cluster-token ${TOKEN}

# For node 2
THIS_NAME=${NAME_2}
THIS_IP=${HOST_2}
etcd --data-dir=data.etcd --name ${THIS_NAME} \
	--initial-advertise-peer-urls http://${THIS_IP}:2380 \
	--listen-peer-urls http://${THIS_IP}:2380 \
	--advertise-client-urls http://${THIS_IP}:2379 \
	--listen-client-urls http://${THIS_IP}:2379 \
	--initial-cluster ${CLUSTER} \
	--initial-cluster-state ${CLUSTER_STATE} \
	--initial-cluster-token ${TOKEN}

# For node 3
THIS_NAME=${NAME_3}
THIS_IP=${HOST_3}
etcd --data-dir=data.etcd --name ${THIS_NAME} \
	--initial-advertise-peer-urls http://${THIS_IP}:2380 \
	--listen-peer-urls http://${THIS_IP}:2380 \
	--advertise-client-urls http://${THIS_IP}:2379 \
	--listen-client-urls http://${THIS_IP}:2379 \
	--initial-cluster ${CLUSTER} \
	--initial-cluster-state ${CLUSTER_STATE} \
	--initial-cluster-token ${TOKEN}
```

Then replace a member with member remove and member add commands:
```
# get member ID
export ETCDCTL_API=3
HOST_1=10.240.0.13
HOST_2=10.240.0.14
HOST_3=10.240.0.15
etcdctl --endpoints=${HOST_1}:2379,${HOST_2}:2379,${HOST_3}:2379 member list

# remove the member
MEMBER_ID=278c654c9a6dfd3b
etcdctl --endpoints=${HOST_1}:2379,${HOST_2}:2379,${HOST_3}:2379 \
	member remove ${MEMBER_ID}

# add a new member (node 4)
export ETCDCTL_API=3
NAME_1=etcd-node-1
NAME_2=etcd-node-2
NAME_4=etcd-node-4
HOST_1=10.240.0.13
HOST_2=10.240.0.14
HOST_4=10.240.0.16 # new member
etcdctl --endpoints=${HOST_1}:2379,${HOST_2}:2379 \
	member add ${NAME_4} \
	--peer-urls=http://${HOST_4}:2380
```

Next, start the new member with --initial-cluster-state existing flag:
```
# [WARNING] If the new member starts from the same disk space,
# make sure to remove the data directory of the old member
#
# restart with 'existing' flag
TOKEN=my-etcd-token-1
CLUSTER_STATE=existing
NAME_1=etcd-node-1
NAME_2=etcd-node-2
NAME_4=etcd-node-4
HOST_1=10.240.0.13
HOST_2=10.240.0.14
HOST_4=10.240.0.16 # new member
CLUSTER=${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_4}=http://${HOST_4}:2380

THIS_NAME=${NAME_4}
THIS_IP=${HOST_4}
etcd --data-dir=data.etcd --name ${THIS_NAME} \
	--initial-advertise-peer-urls http://${THIS_IP}:2380 \
	--listen-peer-urls http://${THIS_IP}:2380 \
	--advertise-client-urls http://${THIS_IP}:2379 \
	--listen-client-urls http://${THIS_IP}:2379 \
	--initial-cluster ${CLUSTER} \
	--initial-cluster-state ${CLUSTER_STATE} \
	--initial-cluster-token ${TOKEN}
```

auth
auth,user,role for authentication:
```
export ETCDCTL_API=3
ENDPOINTS=localhost:2379

etcdctl --endpoints=${ENDPOINTS} role add root
etcdctl --endpoints=${ENDPOINTS} role grant-permission root readwrite foo
etcdctl --endpoints=${ENDPOINTS} role get root

etcdctl --endpoints=${ENDPOINTS} user add root
etcdctl --endpoints=${ENDPOINTS} user grant-role root root
etcdctl --endpoints=${ENDPOINTS} user get root

etcdctl --endpoints=${ENDPOINTS} auth enable
# now all client requests go through auth

etcdctl --endpoints=${ENDPOINTS} --user=root:123 put foo bar
etcdctl --endpoints=${ENDPOINTS} get foo
etcdctl --endpoints=${ENDPOINTS} --user=root:123 get foo
etcdctl --endpoints=${ENDPOINTS} --user=root:123 get foo1
```










