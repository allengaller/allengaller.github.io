# minikube

## Before you begin

To check if virtualization is supported on macOS, run the following command on your terminal.

```
faxi:~ faxi$ sysctl -a | grep machdep.cpu.features
machdep.cpu.features: FPU VME DE PSE TSC MSR PAE MCE CX8 APIC SEP MTRR PGE MCA CMOV PAT PSE36 CLFSH DS ACPI MMX FXSR SSE SSE2 SS HTT TM PBE SSE3 PCLMULQDQ DTES64 MON DSCPL VMX EST TM2 SSSE3 FMA CX16 TPR PDCM SSE4.1 SSE4.2 x2APIC MOVBE POPCNT AES PCID XSAVE OSXSAVE SEGLIM64 TSCTMR AVX1.0 RDRAND F16C
```

If you see VMX in the output, the VT-x feature is supported on your OS.

## Installing

### Install kubectl
Make sure you have kubectl installed. 
https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-macos

#### Install kubectl binary with curl on macOS

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl
```
```
chmod +x ./kubectl
```

```
sudo mv ./kubectl /usr/local/bin/kubectl
```

```
faxi:~ faxi$ kubectl version
Client Version: version.Info{Major:"1", Minor:"15", GitVersion:"v1.15.2", GitCommit:"f6278300bebbb750328ac16ee6dd3aa7d3549568", GitTreeState:"clean", BuildDate:"2019-08-05T09:23:26Z", GoVersion:"go1.12.5", Compiler:"gc", Platform:"darwin/amd64"}
The connection to the server localhost:8080 was refused - did you specify the right host or port?
```


### Install a Hypervisor
If you do not already have a hypervisor installed, install one of these now:

• HyperKit

• VirtualBox

• VMware Fusion

### Install minikube with binary

```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64 \
  && chmod +x minikube
```

executable:
```
sudo mv minikube /usr/local/bin
```

### START Deployment

```
minikube start
```

or

```
minikube delete
```

```
faxi:~ faxi$ minikube start
😄  minikube v1.3.0 on Darwin 10.14.6
💡  Tip: Use 'minikube start -p <name>' to create a new cluster, or 'minikube delete' to delete this one.
🔄  Starting existing virtualbox VM for "minikube" ...
⌛  Waiting for the host to be provisioned ...
🐳  Preparing Kubernetes v1.15.2 on Docker 18.09.8 ...
💾  Downloading kubelet v1.15.2
💾  Downloading kubeadm v1.15.2
🔄  Relaunching Kubernetes using kubeadm ...
⌛  Waiting for: apiserver proxy etcd scheduler controller dns
🏄  Done! kubectl is now configured to use "minikube"
```

```
faxi:~ faxi$ minikube
Minikube is a CLI tool that provisions and manages single-node Kubernetes clusters optimized for development workflows.

Basic Commands:
  start          Starts a local kubernetes cluster
  status         Gets the status of a local kubernetes cluster
  stop           Stops a running local kubernetes cluster
  delete         Deletes a local kubernetes cluster
  dashboard      Access the kubernetes dashboard running within the minikube cluster

Images Commands:
  docker-env     Sets up docker env variables; similar to '$(docker-machine env)'
  cache          Add or delete an image from the local cache.

Configuration and Management Commands:
  addons         Modify minikube's kubernetes addons
  config         Modify minikube config
  profile        Profile gets or sets the current minikube profile
  update-context Verify the IP address of the running cluster in kubeconfig.

Networking and Connectivity Commands:
  service        Gets the kubernetes URL(s) for the specified service in your local cluster
  tunnel         tunnel makes services of type LoadBalancer accessible on localhost

Advanced Commands:
  mount          Mounts the specified directory into minikube
  ssh            Log into or run a command on a machine with SSH; similar to 'docker-machine ssh'
  kubectl        Run kubectl

Troubleshooting Commands:
  ssh-key        Retrieve the ssh identity key path of the specified cluster
  ip             Retrieves the IP address of the running cluster
  logs           Gets the logs of the running instance, used for debugging minikube, not user code
  update-check   Print current and latest version number
  version        Print the version of minikube

Other Commands:
  completion     Outputs minikube shell completion for the given shell (bash or zsh)

Use "minikube <command> --help" for more information about a given command.
```
### Start

https://kubernetes.io/docs/setup/learning-environment/minikube/

```
kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.10 --port=8080
```

```
faxi:~ faxi$ kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.10 --port=8080
kubectl run --generator=deployment/apps.v1 is DEPRECATED and will be removed in a future version. Use kubectl run --generator=run-pod/v1 or kubectl create instead.
deployment.apps/hello-minikube created
```

```
faxi:~ faxi$ kubectl expose deployment hello-minikube --type=NodePort
service/hello-minikube exposed
```

```
faxi:~ faxi$ kubectl get pod
NAME                              READY   STATUS    RESTARTS   AGE
hello-minikube-856979d68c-64rkz   1/1     Running   0          66s
```

```
faxi:~ faxi$ minikube service hello-minikube --url
http://192.168.99.100:32511
```

Browser shows:
```
Hostname: hello-minikube-856979d68c-64rkz

Pod Information:
	-no pod information available-

Server values:
	server_version=nginx: 1.13.3 - lua: 10008

Request Information:
	client_address=172.17.0.1
	method=GET
	real path=/
	query=
	request_version=1.1
	request_scheme=http
	request_uri=http://192.168.99.100:8080/

Request Headers:
	accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
	accept-encoding=gzip, deflate
	accept-language=zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
	connection=keep-alive
	host=192.168.99.100:32511
	upgrade-insecure-requests=1
	user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36

Request Body:
	-no body in request-
```
### Clean up

```
kubectl delete services hello-minikube
```

```
kubectl delete deployment hello-minikube
```

```
minikube stop
```

```
minikube delete
```

### Dashboard

![Dashboard](https://github.com/kubernetes/dashboard/raw/master/docs/images/dashboard-ui.png)

[Github](https://github.com/kubernetes/dashboard)

```
minikube dashboard
```

Deploy
```
faxi:~ faxi$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta1/aio/deploy/recommended.yaml
namespace/kubernetes-dashboard created
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/kubernetes-metrics-scraper created
```
```
faxi:~ faxi$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
secret/kubernetes-dashboard-certs created
serviceaccount/kubernetes-dashboard created
role.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
service/kubernetes-dashboard configured
The Deployment "kubernetes-dashboard" is invalid: spec.selector: Invalid value: v1.LabelSelector{MatchLabels:map[string]string{"k8s-app":"kubernetes-dashboard"}, MatchExpressions:[]v1.LabelSelectorRequirement(nil)}: field is immutable
```

To access Dashboard from your local workstation you must create a secure channel to your Kubernetes cluster. Run the following command:

```
$ kubectl proxy
```

```
http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/
```

* ERROR
无法打开 https://stackoverflow.com/questions/52893111/no-endpoints-available-for-service-kubernetes-dashboard
```
faxi:~ faxi$ kubectl -n kube-system -l=k8s-app=kube-dns get pods
NAME                       READY   STATUS    RESTARTS   AGE
coredns-5c98db65d4-4r5vd   1/1     Running   1          26m
coredns-5c98db65d4-m2zn4   1/1     Running   1          26m
```

```
faxi:~ faxi$ kubectl get pods --all-namespaces
NAMESPACE              NAME                                          READY   STATUS             RESTARTS   AGE
default                hello-minikube-856979d68c-64rkz               1/1     Running            0          19m
kube-system            coredns-5c98db65d4-4r5vd                      1/1     Running            1          27m
kube-system            coredns-5c98db65d4-m2zn4                      1/1     Running            1          27m
kube-system            etcd-minikube                                 1/1     Running            0          26m
kube-system            kube-addon-manager-minikube                   1/1     Running            0          26m
kube-system            kube-apiserver-minikube                       1/1     Running            0          26m
kube-system            kube-controller-manager-minikube              1/1     Running            0          26m
kube-system            kube-proxy-hb4kj                              1/1     Running            0          27m
kube-system            kube-scheduler-minikube                       1/1     Running            0          26m
kube-system            kubernetes-dashboard-7b8ddcb5d6-vr4kf         0/1     CrashLoopBackOff   7          12m
kube-system            storage-provisioner                           1/1     Running            1          27m
kubernetes-dashboard   kubernetes-dashboard-5c8f9556c4-npvwf         1/1     Running            0          8m56s
kubernetes-dashboard   kubernetes-metrics-scraper-86456cdd8f-gl6ws   1/1     Running            0          8m56s
```

![init](/topic/k8s/deployment/pic/dashboard-init.jpg)

```
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login
```

