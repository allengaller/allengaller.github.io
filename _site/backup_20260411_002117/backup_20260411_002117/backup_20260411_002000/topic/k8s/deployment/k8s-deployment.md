# Kubernetes deployment

## Reference
* [Official document](https://kubernetes.io/docs/home/)
* [Install the **kubeadm** setup tool](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
* Learning environment
* Production environment

* [HA Setup](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/)

* [Alibaba Cloud Container Service](https://help.aliyun.com/document_detail/86420.html)

## Tool
* **kubeadm**: the command to bootstrap the cluster.
* **kubelet**: the component that runs on all of the machines in your cluster and does things like starting pods and containers.
* **kubectl**: the command line util to talk to your cluster.

### kubeadmin

kubeadm helps you bootstrap a minimum viable Kubernetes cluster that conforms to best practices. With kubeadm, your cluster should pass Kubernetes Conformance tests. Kubeadm also supports other cluster lifecycle functions, such as upgrades, downgrade, and managing bootstrap tokens.

kubeadm is designed to be a simple way for new users to start trying Kubernetes out, possibly for the first time, a way for existing users to test their application on and stitch together a cluster easily, and also to be a building block in other ecosystem and/or installer tool with a larger scope.

[Installing runtime](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

CentOS:

官方文档
```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

# Set SELinux in permissive mode (effectively disabling it)
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

systemctl enable --now kubelet
```

使用阿里云开源镜像站
```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
setenforce 0
yum install -y kubelet kubeadm kubectl
systemctl enable kubelet && systemctl start kubelet
```






[CREATE CLUSTER](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

### minikube

[Installing minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)

```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube
```

### kubectl

[INSTALL](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

