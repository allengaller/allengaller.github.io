# etcd

Distributed reliable key-value store for the most critical data of a distributed system.
KV存储仓库，用于配置共享和服务发现，使用Go语言编写，通过Raft来保证一致性，提供HTTP+JSON接口。特点：简单、安全、快速、可靠。前辈是zookeeper, 备份方案是consul。

[deployment](/topic/cncf/etcd/etcd-deployment.md)

## links

[official website](https://etcd.io/)
[github](https://github.com/etcd-io/etcd)
[play](http://play.etcd.io/play)

## features

* Simple interface: Read and write values using standard HTTP tools, such as curl
* Key-value storage: Store data in hierarchically organized directories, as in a standard filesystem
* Watch for changes: Watch specific keys or directories for changes and react to changes in values

## about

etcd is a strongly consistent, distributed key-value store that provides a reliable way to store data that needs to be accessed by a distributed system or cluster of machines. It gracefully handles leader elections during network partitions and can tolerate machine failure, even in the leader node.

Applications of any complexity, from a simple web app to Kubernetes, can read data from and write data into etcd.

Your applications can read from and write data into etcd. A simple use case is storing database connection details or feature flags in etcd as key-value pairs. These values can be watched, allowing your app to reconfigure itself when they change. Advanced uses take advantage of etcd’s consistency guarantees to implement database leader elections or perform distributed locking across a cluster of workers.

etcd is open source, available on GitHub, and backed by the Cloud Native Computing Foundation.

## 主要应用场景

1. 服务发现
2. 集群监控
3. 负载均衡
4. 消息发布与订阅
5. 分布式通知与协调
6. 分布式锁与竞选
7. 分布式队列