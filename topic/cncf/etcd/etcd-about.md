# About Etcd

## Links
[Github](https://github.com/etcd-io/etcd)
[Official website](https://etcd.io/)

## Features

* Simple interface

	Read and write values using standard HTTP tools, such as curl

* Key-value storage

	Store data in hierarchically organized directories, as in a standard filesystem

* Watch for changes

	Watch specific keys or directories for changes and react to changes in values

## About

etcd is a strongly consistent, distributed key-value store that provides a reliable way to store data that needs to be accessed by a distributed system or cluster of machines. It gracefully handles leader elections during network partitions and can tolerate machine failure, even in the leader node.

Applications of any complexity, from a simple web app to Kubernetes, can read data from and write data into etcd.

Your applications can read from and write data into etcd. A simple use case is storing database connection details or feature flags in etcd as key-value pairs. These values can be watched, allowing your app to reconfigure itself when they change. Advanced uses take advantage of etcd’s consistency guarantees to implement database leader elections or perform distributed locking across a cluster of workers.

etcd is open source, available on GitHub, and backed by the Cloud Native Computing Foundation.