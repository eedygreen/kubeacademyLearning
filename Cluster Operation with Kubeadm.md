# Cluster Operation with Kubeadm

Kubeadm is a tool built to provide `kubeadm init` and `kubeadm join` as best-practice "fast paths" for creating Kubernetes clusters.

kubeadm performs the actions necessary to get a minimum viable cluster up and running. By design, it cares only about bootstrapping, not about provisioning machines. Likewise, installing various nice-to-have addons, like the Kubernetes Dashboard, monitoring solutions, and cloud-specific addons, is not in scope.

Instead, we expect higher-level and more tailored tooling to be built on top of kubeadm, and ideally, using kubeadm as the basis of all deployments will make it easier to create conformant clusters.

## How to install

To install kubeadm, see the [installation guide](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm).

## What's next

- [kubeadm init](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init) to bootstrap a Kubernetes control-plane node
- [kubeadm join](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join) to bootstrap a Kubernetes worker node and join it to the cluster
- [kubeadm upgrade](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-upgrade) to upgrade a Kubernetes cluster to a newer version
- [kubeadm config](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-config) if you initialized your cluster using kubeadm v1.7.x or lower, to configure your cluster for `kubeadm upgrade`
- [kubeadm token](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-token) to manage tokens for `kubeadm join`
- [kubeadm reset](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-reset) to revert any changes made to this host by `kubeadm init` or `kubeadm join`
- [kubeadm version](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-version) to print the kubeadm version
- [kubeadm alpha](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-alpha) to preview a set of features made available for gathering feedback from the community

**Installing Kubeadm**

```shell
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```



**Initializing Kubeadm**

```shell
kubeadm init 

kubeadm init --pod-network-cidr=10.0.12.3/16 # option to provide network
```



**Create the Configuration Directory**

```shell
mkdir -p $HOME/.kube #create the directory

sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/cofig # copy the configuration file to the new created .kube directory

chown $(id -u):$(id -g) $HOME/.kube/config # change the ownership of the directory
```



*Note: To use different configuration use the command `kubectl --kubeconfig=./ptha_config_file`*

```shell
kubectl --kubeconfig=./kube23/config get nodes

kubectl --kubeconfig=./kube23/config get clusters

kubectl --kubeconfig=./kube23/config get pods
```

**Secrets**

*Note: To get the secrets*

```shell
kubectl get secrets # this list all the available secrets in a cluster

kubetctl get secrets secrets_name # to get a specific secrets
```



**Deploy an application**

```shell
kubectl apply application.yanl
```



**Join the cluster**

Use the `kubeadm join` command to join any worker node

```shell
kubeadm join ip_address:port_number --token token-id --discovery-token-ca-cert-hash sha_value
```

**Get the nodes that has been joined**

```shell
kubectl get nodes
```



Add the CNI 'calico' network node

```shell
kubectl apply -f calico.yanl
```



*Note: you an always ssh to any worker node to join the other using the kubeadm `kubeadm join` command*



**Custom Resources Definition (CRDs)**

```shell
kubectl get crds
```

```shell
NAME                                              CREATED AT
alertmanagers.monitoring.coreos.com               2020-12-23T19:56:01Z
applications.app.k8s.io                           2020-12-23T19:54:23Z
clusterconfigurations.installer.kubesphere.io     2020-12-23T19:53:13Z
clusters.cluster.kubesphere.io                    2020-12-23T19:54:23Z
dashboards.monitoring.kubesphere.io               2020-12-23T19:56:27Z
devopsprojects.devops.kubesphere.io               2020-12-23T19:54:23Z
emailconfigs.notification.kubesphere.io           2020-12-23T19:56:22Z
emailreceivers.notification.kubesphere.io         2020-12-23T19:56:22Z
eniconfigs.crd.k8s.amazonaws.com                  2020-12-23T16:30:04Z
globalrolebindings.iam.kubesphere.io              2020-12-23T19:54:23Z
globalroles.iam.kubesphere.io                     2020-12-23T19:54:23Z
loginrecords.iam.kubesphere.io                    2020-12-23T19:54:23Z
namespacenetworkpolicies.network.kubesphere.io    2020-12-23T19:54:24Z
notificationmanagers.notification.kubesphere.io   2020-12-23T19:56:22Z
pipelines.devops.kubesphere.io                    2020-12-23T19:54:23Z
podmonitors.monitoring.coreos.com                 2020-12-23T19:56:02Z
prometheuses.monitoring.coreos.com                2020-12-23T19:56:02Z
prometheusrules.monitoring.coreos.com             2020-12-23T19:56:03Z
provisionercapabilities.storage.kubesphere.io     2020-12-23T19:54:25Z
rolebases.iam.kubesphere.io                       2020-12-23T19:54:23Z
s2ibinaries.devops.kubesphere.io                  2020-12-23T19:54:23Z
s2ibuilders.devops.kubesphere.io                  2020-12-23T19:54:23Z
s2ibuildertemplates.devops.kubesphere.io          2020-12-23T19:54:23Z
s2iruns.devops.kubesphere.io                      2020-12-23T19:54:23Z
securitygrouppolicies.vpcresources.k8s.aws        2020-12-23T16:30:07Z
servicemonitors.monitoring.coreos.com             2020-12-23T19:56:03Z
servicepolicies.servicemesh.kubesphere.io         2020-12-23T19:54:24Z
slackconfigs.notification.kubesphere.io           2020-12-23T19:56:22Z
slackreceivers.notification.kubesphere.io         2020-12-23T19:56:22Z
storageclasscapabilities.storage.kubesphere.io    2020-12-23T19:54:25Z
strategies.servicemesh.kubesphere.io              2020-12-23T19:54:24Z
thanosrulers.monitoring.coreos.com                2020-12-23T19:56:03Z
users.iam.kubesphere.io                           2020-12-23T19:54:23Z
volumesnapshotclasses.snapshot.storage.k8s.io     2020-12-23T19:54:31Z
volumesnapshotcontents.snapshot.storage.k8s.io    2020-12-23T19:54:31Z
volumesnapshots.snapshot.storage.k8s.io           2020-12-23T19:54:31Z
wechatconfigs.notification.kubesphere.io          2020-12-23T19:56:23Z
wechatreceivers.notification.kubesphere.io        2020-12-23T19:56:23Z
workspacerolebindings.iam.kubesphere.io           2020-12-23T19:54:24Z
workspaceroles.iam.kubesphere.io                  2020-12-23T19:54:24Z
workspaces.tenant.kubesphere.io                   2020-12-23T19:54:25Z
workspacetemplates.tenant.kubesphere.io           2020-12-23T19:54:25Z

```

What is a Management Cluster 

What is Workload Cluster?