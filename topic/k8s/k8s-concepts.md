# k8s concepts


[Official website](https://kubernetes.io/docs/concepts/)
[中英名词对比](https://help.aliyun.com/document_detail/113088.html)
[Kubernetes 相关概念](https://help.aliyun.com/document_detail/86742.html)

## 集群

一个集群指容器运行所需要的云资源组合，关联了若干服务器节点、负载均衡、专有网络等云资源。

## 节点

一台服务器（可以是虚拟机实例或者物理服务器）已经安装了 Docker Engine，可以用于部署和管理容器；容器服务的 Agent 程序会安装到节点上并注册到一个集群上。集群中的节点数量可以伸缩。

## 容器

一个通过 Docker 镜像创建的运行实例，一个节点可运行多个容器。

## 镜像

Docker 镜像是容器应用打包的标准格式，在部署容器化应用时可以指定镜像，镜像可以来自于 Docker Hub，阿里云镜像服务，或者用户的私有 Registry。镜像 ID 可以由镜像所在仓库 URI 和镜像 Tag（缺省为 latest）唯一确认。


## 管理节点（Master Node）

管理节点是Kubernetes集群的管理者，运行着的服务包括kube-apiserver、kube-scheduler、kube-controller-manager、etcd和容器网络等组件。一般3个管理节点组成HA的架构。

## 工作节点（Worker Node）

工作节点是Kubernetes集群中承担工作负载的节点，可以是虚拟机也可以是物理机。工作节点承担实际的 Pod 调度以及与管理节点的通信等。一个工作节点上的服务包括Docker运行时环境、kubelet、Kube-Proxy以及其它一些可选的Addon组件。

## 命名空间（Namespace）

命名空间为 Kubernetes 集群提供虚拟的隔离作用。Kubernetes 集群初始有 3 个命名空间，分别是默认命名空间 default、系统命名空间 kube-system 和 kube-public ，除此以外，管理员可以创建新的命名空间以满足需求。

## Pod

Pod是 Kubernetes 部署应用或服务的最小的基本单位。一个Pod 封装多个应用容器（也可以只有一个容器）、存储资源、一个独立的网络 IP 以及管理控制容器运行方式的策略选项。

## 副本控制器（Replication Controller，RC）

RC 确保任何时候 Kubernetes 集群中有指定数量的 pod 副本(replicas)在运行。通过监控运行中的 Pod 来保证集群中运行指定数目的 Pod 副本。指定的数目可以是多个也可以是1个；少于指定数目，RC 就会启动运行新的 Pod 副本；多于指定数目，RC 就会终止多余的 Pod 副本。

## 副本集（Replica Set，RS）

ReplicaSet（RS）是 RC 的升级版本，唯一区别是对选择器的支持，RS 能支持更多种类的匹配模式。副本集对象一般不单独使用，而是作为 Deployment 的理想状态参数使用。

## 部署（Deployment）

部署表示用户对 Kubernetes 集群的一次更新操作。部署比 RS 应用更广，可以是创建一个新的服务，更新一个新的服务，也可以是滚动升级一个服务。滚动升级一个服务，实际是创建一个新的 RS，然后逐渐将新 RS 中副本数增加到理想状态，将旧 RS 中的副本数减小到 0 的复合操作；这样一个复合操作用一个RS是不太好描述的，所以用一个更通用的 Deployment 来描述。不建议您手动管理利用 Deployment 创建的 RS。

## 服务（Service）

Service 也是 Kubernetes 的基本操作单元，是真实应用服务的抽象，每一个服务后面都有很多对应的容器来提供支持，通过 Kube-Proxy 的 port 和服务 selector 决定服务请求传递给后端的容器，对外表现为一个单一访问接口，外部不需要了解后端如何运行，这给扩展或维护后端带来很大的好处。

## 标签（labels）

Labels 的实质是附着在资源对象上的一系列 Key/Value 键值对，用于指定对用户有意义的对象的属性，标签对内核系统是没有直接意义的。标签可以在创建一个对象的时候直接赋予，也可以在后期随时修改，每一个对象可以拥有多个标签，但 key 值必须唯一。

## 存储卷（Volume）

Kubernetes 集群中的存储卷跟 Docker 的存储卷有些类似，只不过 Docker 的存储卷作用范围为一个容器，而 Kubernetes 的存储卷的生命周期和作用范围是一个 Pod。每个 Pod 中声明的存储卷由 Pod 中的所有容器共享。支持使用 Persistent Volume Claim 即 PVC 这种逻辑存储，使用者可以忽略后台的实际存储技术，具体关于 Persistent Volumn(pv)的配置由存储管理员来配置。

## 持久存储卷（Persistent Volume，PV）和持久存储卷声明（Persistent Volume Claim，PVC）

PV 和 PVC 使得 Kubernetes 集群具备了存储的逻辑抽象能力，使得在配置 Pod 的逻辑里可以忽略对实际后台存储技术的配置，而把这项配置的工作交给 PV 的配置者。存储的 PV 和 PVC 的这种关系，跟计算的 Node 和 Pod 的关系是非常类似的；PV 和 Node 是资源的提供者，根据集群的基础设施变化而变化，由 Kubernetes 集群管理员配置；而 PVC 和 Pod是资源的使用者，根据业务服务的需求变化而变化，由 Kubernetes 集群的使用者即服务的管理员来配置。

## Ingress

Ingress 是授权入站连接到达集群服务的规则集合。你可以通过 Ingress 配置提供外部可访问的 URL、负载均衡、SSL、基于名称的虚拟主机等。用户通过 POST Ingress 资源到 API server 的方式来请求 Ingress。 Ingress controller 负责实现 Ingress，通常使用负载均衡器，它还可以配置边界路由和其他前端，这有助于以 HA 方式处理流量。