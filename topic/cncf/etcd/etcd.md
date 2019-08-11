# etcd

[deployment](/topic/cncf/etcd/etcd-deployment.md)

* Distributed reliable key-value store for the most critical data of a distributed system.
KV存储仓库，用于配置共享和服务发现，使用Go语言编写，通过Raft来保证一致性，提供HTTP+JSON接口。特点：简单、安全、快速、可靠。前辈是zookeeper, 备份方案是consul。

## links

[official website](https://etcd.io/)

[github](https://github.com/etcd-io/etcd)

[play](http://play.etcd.io/play)

## features

* Simple interface: Read and write values using standard HTTP tools, such as curl
* Key-value storage: Store data in hierarchically organized directories, as in a standard filesystem
* Watch for changes: Watch specific keys or directories for changes and react to changes in values

## about

* etcd is a strongly consistent, distributed key-value store that provides a reliable way to store data that needs to be accessed by a distributed system or cluster of machines. It gracefully handles leader elections during network partitions and can tolerate machine failure, even in the leader node.

* Applications of any complexity, from a simple web app to Kubernetes, can read data from and write data into etcd.

* Your applications can read from and write data into etcd. A simple use case is storing database connection details or feature flags in etcd as key-value pairs. These values can be watched, allowing your app to reconfigure itself when they change. Advanced uses take advantage of etcd’s consistency guarantees to implement database leader elections or perform distributed locking across a cluster of workers.

* etcd is open source, available on GitHub, and backed by the Cloud Native Computing Foundation.

## main usage

* 服务发现
* 集群监控
* 负载均衡
* 消息发布与订阅
* 分布式通知与协调
* 分布式锁与竞选
* 分布式队列

## Tools (3.3.12)

* etcdctl - A command line client for etcd
* etcd-backup - A powerful command line utility for dumping/restoring etcd - Supports v2
* etcd-dump - Command line utility for dumping/restoring etcd.
* etcd-fs - FUSE filesystem for etcd
* etcddir - Realtime sync etcd and local directory. Work with windows and linux.
* etcd-browser - A web-based key/value editor for etcd using AngularJS
* etcd-lock - Master election & distributed r/w lock implementation using etcd - Supports v2
* etcd-console - A web-base key/value editor for etcd using PHP
* etcd-viewer - An etcd key-value store editor/viewer written in Java
* etcdtool - Export/Import/Edit etcd directory as JSON/YAML/TOML and Validate directory using JSON schema
* etcd-rest - Create generic REST API in Go using etcd as a backend with validation using JSON schema
* etcdsh - A command line client with support of command history and tab completion. Supports v2
* etcdloadtest - A command line load test client for etcd version 3.0 and above.
* lucas - A web-based key-value viewer for kubernetes etcd3.0+ cluster.