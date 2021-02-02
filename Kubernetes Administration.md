# Kubernetes Administration

### View the context

```shell
kubectl config view
```



```shell
 kubectl config get-clusters
```



```shell
kubectl config current-context
```

### Create New Context

Let's create a new `kubectl` context using the existing `kubernetes-admin` user. Type the below command:

```shell
kubectl config set-context dev-context --cluster kubernetes --user=kubernetes-admin
```

### Get contexts

```shell
kubectl config get-contexts
```

### Switch to dev-context

```shell
kubectl config use-context dev-context
```

**view the context**

```shell
kubectl config get-contexts
```



**Switch back**

Let's switch back to the `kubernetes-admin@kubernetes` context by typing the below command:

```shell
kubectl config use-context kubernetes-admin@kubernetes
```

### Switch Context `kubectx` the easy way

We can create a script that does the switching kubectx.sh

```shell
#!/bin/bash

cd ~/

echo "You are on the $PWD directory"
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens
```

 List the Contexts

```shell
kubectx
```

Switch Context

```shell
kubectx dev-context
```

This script save us a lot time typing 

```shell
kubectl config  use-context CONTEXTNAME
```



### Create Namespaces

- **Imperative method** is the using the kubectl 

```shell
kubectl create namespac frontend
```

```
kubectl create ns frontend
```



- **Declarative method** is using the yaml file.

  - Option 1: Manually create the yaml file and specify the *namespace* in specs
  - Options 2: Generate the manifest file via the `kubectl` command

  ```shell
  kubectl create namespace backend -o yaml --dry-run >~ns-backend.yaml
  ```

  Note: The --dry-run flag allows you to preview the the object without creating it and makes no change to the cluster. The best way to visualize and validate without introducing changes.

  ```
  cat ~/ns-backend.yaml
  ```

   Apply the file to create the namespace

  ```shell
  kubectl apply -f ~/ns-backend.yaml
  ```

  View the changes

  ```shel
  kubectl get ns
  ```

  

### Create Resources inside a Namespace

Let's deploy a single `redis` container into the `backend` namespace using `kubectl run` with the `--restart=Never`. Type the below command:

```shell
kubectl run redis --image-redis -n backend --restart=Never
```

*Note: The `--restart=Never` flag tells the `kubectl run` command to create a single pod.*

Let's use another method to deploy a single `nginx` container application in the `frontend` namespace using `kubectl run` with the `--generator` flag. Type the below command:

```shell
kubectl run nginx --generator=run-pod/v1 --image=nginx --namespace frontend
```

*Note: The `--generator` flag tells the `kubectl run` command to pin the resource to a specific apiVersion specification. In this case apiVersion:v1 and kind:pod. This flag is **NOT** widely used and may get depracated in future version releases*



### Switch Between Namespaces

To avoid providing the `--namespace` flag with each time we type `kubectl ` command when outside of the default namespace. 

```shell
kubectl config set-context --current --namespace=frontend
```

We can now list the pods in the `frontend` namespace without adding the `--namespace` or `-n` flag:

```shell
kubectl get pods
```

If you are constantly switching between namespaces and want to avoid using the long `kubectl` command above, then the `kubens` plugin becomes handy. It is bundled with the `kubectx` utility when installed using a package management tool such as yum, apt, dnf, brew, etc.

These two plug-ins can also be installed via `krew`, which is a package manager tool for `kubectl` plug-ins.



#### Install kubens to switch between namespaces

```shell
#!/bin/bash

cd ~/

echo "You are on the $PWD directory"
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens		# kubens
```

To view the namespaces

```shell
kubens
```

Switch to the frontend namespace

```shell
kubens frontend
```

List the pods

```shell
kubectl get pods
```

Switch to default

```shell
kubens default
```

Clean up the environment

```shell
kubectl delete pod nginx -n frontend
```

```shell
kubectl delete pod redis -n backend
```



### Find resource with --selector

You can use the `--selector` flag to filter and find resources based on their assigned labels. Let's see how that works.

```shell
kubectl get pods -n frontend --show-labels
```

Output

```
controlplane $ kubectl get pods -n frontend --show-labels
NAME                                  READY   STATUS    RESTARTS   AGE     LABELS
frontend-deployment-7bb7f6687-2ckb9   1/1     Running   0          6m29s   app=web,pod-template-hash=7bb7f6687
frontend-deployment-7bb7f6687-bvm7l   1/1     Running   0          6m29s   app=web,pod-template-hash=7bb7f6687
frontend-deployment-7bb7f6687-rn7bm   1/1     Running   0          6m29s   app=web,pod-template-hash=7bb7f6687
haproxy-deployment-788ff46cb4-g2sdw   1/1     Running   0          6m29s   app=haproxy,pod-template-hash=788ff46cb4
haproxy-deployment-788ff46cb4-tmfkl   1/1     Running   0          6m29s   app=haproxy,pod-template-hash=788ff46cb4
haproxy-deployment-788ff46cb4-vdvlk   1/1     Running   0          6m29s   app=haproxy,pod-template-hash=788ff46cb4
```



Now, let's find all the pods that have the label `app: web` in the `frontend` namespace:

```shell
kubectl get pods -n frontend --selector=app=web
```

Output

```
controlplane $ kubectl get pods -n frontend --selector=app=web
NAME                                  READY   STATUS    RESTARTS   AGE
frontend-deployment-7bb7f6687-2ckb9   1/1     Running   0          7m59s
frontend-deployment-7bb7f6687-bvm7l   1/1     Running   0          7m59s
frontend-deployment-7bb7f6687-rn7bm   1/1     Running   0          7m59s

```



You can also use the `-l` flag, which represents `label` and is equivalent to the `--selector` flag. label with app=haproxy

```shell
kubectl get pods -n frontend -l app=haproxy
```

Output

```
controlplane $ kubectl get pods -n frontend -l app=haproxy
NAME                                  READY   STATUS    RESTARTS   AGE
haproxy-deployment-788ff46cb4-g2sdw   1/1     Running   0          9m10s
haproxy-deployment-788ff46cb4-tmfkl   1/1     Running   0          9m10s
haproxy-deployment-788ff46cb4-vdvlk   1/1     Running   0          9m10s
```



The `--selector` flag can also be used to find resources that do **NOT** have a certain label. To illustrate this, let's find nodes within our cluster that do **NOT** have the taint label: `node-role.kubernetes.io/master`. Type the below command:

```shell
kubectl get nodes --selector='!node-role.kubernetes.io/master'
```

Output

```
controlplane $ kubectl get nodes --selector='!node-role.kubernetes.io/master'
NAME     STATUS   ROLES    AGE    VERSION
node01   Ready    <none>   132m   v1.14.0
```



As you can see, the `--selector` or `-l` flags could come in very handy when identifying thousands of kubernetes resources with differing labels.



### Use jsonpath to find/filter resources

- Create or form the jsonpath query. In our case, the query would be the following:

  `'{.items[*].metadata.name}{.items[*].status.capacity.cpu}'`

- Pass the query to the jsonpath option of the `kubectl` command. Type the below command:

  ```shell
  kubectl get nodes -o=jsonpath='{.items[*].metadata.name} {.items[*].status.capacity.cpu}'
  ```

As you may notice, the output does not look pretty. What if we add a `\n` (newline character) between the two JSONPath pairs as:

```shell
kubectl get nodes -o=jsonpath='{.items[*].metadata.name} {.items[*].status.capacity.cpu}{"\n"}'
```



### Use Loop/Range in JSONPath with Kubectl

To achieve this, we would use the range JSONPath operator to iterate through each item (nodes in this case) and use tabulation `\t` as well as new line `\n` characters to achieve the desired output.

To do this in JSONPath, we would use the `range` and `end` operators as shown below:

```
{range  .items[*]}
    { .metadata.name}{"\t"}
    {.status.capacity.cpu}{"\n"}
{end}
```

Let's now merge the above command into one line and pass it to the `kubectl` `-o=jsonpath` option. Below, is the result of the command. Go ahead and type the below command and inspect its output:

```
kubectl get nodes -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.capacity.cpu}{"\n"}{end}'
```

Output

```
controlplane $ kubectl get nodes -o=jsonpath='{range  .items[*]}{.metadata.name}{"\t"}{.status.capacity.cpu}{"\n"}{end}'
controlplane    2
node01  2
```



### Format output with custom-columns

If we want to get output with nicely formatted column headers, then JSONPath's custom columns is the best option.

Custom-columns are easier to use than the range operator. Here is how to use custom-columns with `kubectl`:

format

```shell
kubectl get RESOURCE -o=custom-columns=COLUMN_HEADER:.JSONPATH QUERY
```

Now, let's assume we want to get all nodes within our cluster and nicely format the output with a column header called NAME. To do that, type the below command

```shell
kubectl get nodes -o=custom-columns=Name:.metadata.name
```

Output

```shell
controlplane $ kubectl get nodes -o=custom-columns=NAME:.metadata.nameNAME
controlplane
node01
```

You can add additional columns to the above command by adding JSONPath pairs (COLUMN HEADER:.metadata) separated by a comma.

In the below command example, we are adding a CPU column header. Type the below command:

```shell
kubectl get nodes -o=custom-columns=Name:.metadata.name,CPU:.status.capacity
```

Output

```shell
controlplane $ kubectl get nodes -o=custom-columns=NAME:.metadata.name,CPU:.status.capacity.cpuNAME           CPU
controlplane   2
node01         2
```



let's find all the pods that were deployed with the label `image:nginx:1.16` and output them in a tabulated format with column headers POD_NAME and IMAGE_VER:

```shell
kubectl get pods -n frontend -o custom-columns=POD_NAME:.metadata.name,IMAGE_VER:.spec.containers[*].image
```

Output

```shell
ontrolplane $ kubectl get pods -n frontend -o custom-columns=POD_NAME:.metadata.name,IMAGE_VER:.spec.containers[*].image
POD_NAME                              IMAGE_VER
frontend-deployment-7bb7f6687-2ckb9   nginx:1.16
frontend-deployment-7bb7f6687-bvm7l   nginx:1.16
frontend-deployment-7bb7f6687-rn7bm   nginx:1.16
haproxy-deployment-788ff46cb4-g2sdw   nginx:1.16
haproxy-deployment-788ff46cb4-tmfkl   nginx:1.16
haproxy-deployment-788ff46cb4-vdvlk   nginx:1.16
controlplane $
```



### Scale Resources

Let's deploy an nginx application in the default namespace using the `kubectl` command line method. Type the below command:

```shell
kubectl create deployment nginx-deployment --image=nginx:1.16
```

````shell
controlplane $ kubectl create deployment nginx-deployment --image=nginx:1.16
deployment.apps/nginx-deployment created
controlplane $ kubectl get deploy nginx-deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGEnginx-deployment   1/1     1            1           25s
controlplane $ kubect get podskubect: command not foundcontrolplane $ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-5ffcd5768b-fc264   1/1     Running   0          83scontrolplane $ kubectl scale deployment nginx-deployment --replicas=5deployment.extensions/nginx-deployment scaled
controlplane $ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-5ffcd5768b-2fb8z   1/1     Running   0          4s
nginx-deployment-5ffcd5768b-4n887   1/1     Running   0          4s
nginx-deployment-5ffcd5768b-fc264   1/1     Running   0          2m13s
nginx-deployment-5ffcd5768b-vb9nd   1/1     Running   0          4s
nginx-deployment-5ffcd5768b-vx94z   1/1     Running   0          4s
controlplane $
````



You can pass the `-w` flag to watch the scaling live.



### Update Resources

In this step, we are going to update the `nginx` image from `nginx:1.16` to `nginx:1.17` with no downtime. We created a deployment in the previous step, which provides a mechanism (`rollingUpdate`) by default.

```shell
controlplane $ kubectl scale deployment/nginx-deployment --replicas=5
deployment.extensions/nginx-deployment scaled
controlplane $ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-5ffcd5768b-2skq2   1/1     Running   0          7s
nginx-deployment-5ffcd5768b-5cs5r   1/1     Running   0          4m35s
nginx-deployment-5ffcd5768b-nc4fw   1/1     Running   0          7s
nginx-deployment-5ffcd5768b-zlstz   1/1     Running   0          7s
nginx-deployment-5ffcd5768b-zlxqn   1/1     Running   0          7s
controlplane $ kubectl get deployment/nginx-deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   5/5     5            5           4m43s
controlplane $
```

Let's filter all the pod names along with their current `nginx` image version using custom-columns:

```shell
controlplane $ kubectl get pods -o custom-columns=Pod_NAME:.metadata.name,IMAGE_VER:.spec.containers[*].image
Pod_NAME                            IMAGE_VER
nginx-deployment-5ffcd5768b-2skq2   nginx:1.16
nginx-deployment-5ffcd5768b-5cs5r   nginx:1.16
nginx-deployment-5ffcd5768b-nc4fw   nginx:1.16
nginx-deployment-5ffcd5768b-zlstz   nginx:1.16
nginx-deployment-5ffcd5768b-zlxqn   nginx:1.16
controlplane $
```

Now, let's proceed with the update. We will add the `--record` flag to capture and record the history of the rollout: 

```shell
kubectl set image deployment/nginx-deployment nginx=nginx:1.17 --record
```

Output

```shell
controlplane $ kubectl set image deployment/nginx-deployment nginx=nginx:1.17 --record
deployment.extensions/nginx-deployment image updated
controlplane $
```

Alternatively, the result above can be achieved by editing the deployment manifest either manually or using the

```shell
kubectl edit deployment deployment_name
```

The deployment will be opened in the default text editor (typically `vim`). Edit the .spec.template.spec.containers[].image key's value by changing the image to `nginx:1.17` and saving the changes. As long as the manifest validates properly, the deployment will be updated in the cluster.

**NOTE:** *Updating the image of a deployment using the imperative `kubectl set image` commands is not best practice. The best practice is to manually edit the deployment manifest file and update the spec.template.spec.containers[].image field, save it, and run the `kubectl apply -f DEPPLYOMET.YAML` command. This way, the deployment manifest file remains the source of truth.*



We can watch the status of the `nginx-deployment` deployment's `rollingUpdate` changes until completion. Type the below command:

```shell
kubectl rollout status -w deployment/nginx-deployment
```

To show the output of the rollout history, type the below command

```shell
kubectl rollout history deployment/nginx-deployment
```

Output

```shell
controlplane $ kubectl rollout status -w deployment/nginx-deployment
deployment "nginx-deployment" successfully rolled out
controlplane $ kubectl rollout history deployment/nginx-deployment
deployment.extensions/nginx-deployment
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deployment/nginx-deployment nginx=nginx:1.17 --record=true

```

```shell
kubectk get pods -o custom-columnsPod_Name:.metadata.name,IMAGE-VER:.spec.containers[*].image
```

```shell
controlplane $ kubectl get pods -o custom-columns=Pod_MAME:.metadata.name,IMAGE-VER:.spec.containers[*].image
Pod_MAME                           IMAGE-VER
nginx-deployment-9f499969f-9285j   nginx:1.17
nginx-deployment-9f499969f-l2psh   nginx:1.17
nginx-deployment-9f499969f-q77cs   nginx:1.17
nginx-deployment-9f499969f-sq99r   nginx:1.17
nginx-deployment-9f499969f-v9zrb   nginx:1.17
controlplane $
```



Undo the update

```shell
controlplane $ kubectl rollout undo deployment/nginx-deployment
deployment.extensions/nginx-deployment rolled back
controlplane $
```

Output

```shell
controlplane $ kubectl rollout undo deployment/nginx-deployment
deployment.extensions/nginx-deployment rolled back

controlplane $ kubectl rollout status -w deployment/nginx-deployment
deployment "nginx-deployment" successfully rolled out

controlplane $ kubectl get pods -o custom-columns=Pod_MAME:.metadata.name,IMAGE-VER:.spec.containers[*].image
Pod_MAME                            IMAGE-VER
nginx-deployment-5ffcd5768b-5mmvv   nginx:1.16
nginx-deployment-5ffcd5768b-5sjxt   nginx:1.16
nginx-deployment-5ffcd5768b-cjxfl   nginx:1.16
nginx-deployment-5ffcd5768b-nw9m6   nginx:1.16
nginx-deployment-5ffcd5768b-p7ww9   nginx:1.16
```

Finally, if you want to update your application with a prior rollout revision, run the `kubectl rollout history` command to show the different configuration revisions. Pick the previous revision number you want to change your application to and run the `kubectl` command with the `--to-revision=n`flag, where `n=revision number` from the rollout history output. Here is the full command you would use: `kubectl rollout undo --to-revision=n`.

Let's change the image version back to `nginx:1.17` once more using this method. Type the below command:

```shell
controlplane $ kubectl rollout history deployment/nginx-deployment
deployment.extensions/nginx-deployment
REVISION  CHANGE-CAUSE
2         kubectl set image deployment/nginx-deployment nginx=nginx:1.17 --record=true
3         <none>

controlplane $ kubectl rollout undo deployment/nginx-deployment --to-revision=2
deployment.extensions/nginx-deployment rolled back
```

**NOTE:** *Using the imperative `kubectl rollout undo` command is not best practice. The best practice is to manually edit the deployment manifest file and update the appropriate field (in this case here, spec.template.spec.containers[].image), save it, and run the `kubectl apply -f DEPPLYOMET.YAML` command. This way, the deployment manifest file remains the source of truth.*



### Patch and label resources

Patching can be used to partially update any kubernetes resources such as nodes, pods, deployments, etc. In this step, we are going to deploy an `nginx` pod with a label of `env: prod` using the `kubectl` command. We will then update the label.

Let's create a pod with a label `env=prod` in the default namespace:

```shell
kubectl run nginx --image=nginx --restart=Never --labels=env=prod
```



```shell
kubectl get pod nginx --show-labels
```



```shell
kubectl patch pod nginx -p '{"metadata":{"lables":{"env":"dev"}}}'
pod/nginx patched (no change)
```

Output

```shell
controlplane $ kubectl run nginx --image=nginx --restart=Never --labels=env=prod
pod/nginx created
controlplane $ kubectl get pod nginx --show-labels
NAME    READY   STATUS    RESTARTS   AGE     LABELS
nginx   1/1     Running   0          2m31s   env=prod
```



We can also use the `kubectl label` command to add a label, update an existing label, or delete a label. Type the below command to update the label `env:dev` to `env:prod`:

```shell
kubectl label pod nginx env=prod --overwrite
```

```shell
kubectl get pod nginx --show-label	
```

To delete the label, append the `-` to `env` , which is the value of the label's key. Type the below command:

```shell
kubectl get pod nginx env-
```

```shell
controlplane $ kubectl get pod nginx --show-labels
NAME    READY   STATUS    RESTARTS   AGE     LABELS
nginx   1/1     Running   0
```



Alternatively, use the `kubectl edit pod nginx` command and manually edit the .metadata.label.env and save your changes.



### Delete Resources

To delete a resource, you can simply run the `kubectl delete RESOURCE_TYPE RESOURCE NAME` command. For example, to delete the single pod resource that we deployed in the previous step, type:

```shell
kubectl delete pod nginx
```

```shell
kubectl delete -f ~/deploy-nginx.yaml
```

```shell
kubectl delete deployment deploy-nginx
```



## Advanced

### kubectl Plugin Setup

In the [kubectl intermediate](https://katacoda.com/mbah-vmw/scenarios/kubectl-intermediate) scenario lab, we introduced you to a few `kubectl` plugins (NS and CTX). Now, we are going to introduce you to `krew`, which is a plugin manager for `kubectl`. We will use `krew` to install various plugins that we will use throughout the scenario. We will be using the following plugins:

- `access-matrix` - shows an RBAC (role based access control) access matrix for server resources
- `ns` - view or change switch namespace contexts
- `ctx` - switch between Kubernetes cluster contexts

For the full list of available plugins, please view them [here](https://github.com/kubernetes-sigs/krew-index/blob/master/plugins.md)



Let's install `krew` by running the `install-krew.sh` script:

```sh
#!/bin/bash

#Downloading  krew from repo"
echo -en "Downloading and installing krew\n"
  set -x; cd "$(mktemp -d)" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/download/v0.3.4/krew.{
tar.gz,yaml}" &&
  tar zxvf krew.tar.gz &&
  KREW=./krew-"$(uname | tr '[:upper:]' '[:lower:]')_amd64" &&
  "$KREW" install --manifest=krew.yaml --archive=krew.tar.gz &&
  "$KREW" update

#Adding it to home user ~/.bashrc file
echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >>~/.bashrc

#source the bashrc and restart bash
source ~/.bashrc
exec bash
```

### kubectl and krew usage

There are currently 80+ plugins that can be installed using the`kubectl krew install` command. Please note, these plugins are not audited for security by the Krew maintainers, therefore running them is at your own risk.

Let's discover some of these plugins:

```shell
kubectl krew search
```

| Krew Plug-in    | Description                                      |
| :-------------- | :----------------------------------------------- |
| `access-matrix` | Show an RBAC access matrix for server resources  |
| `ca-cert`       | Pretty print the current cluster certificate.    |
| `ctx`           | Switch between Kubernetes cluster contexts       |
| `iexec`         | Interactive selection tool for kubectl exec      |
| `images`        | Show container images used in the cluster        |
| `ns`            | Switch between Kubernetes namespaces             |
| `pod-logs`      | Display a list of pods to get logs from          |
| `whoami`        | Shows the subject that's currently authenticated |
| `who-can`       | Shows which subjects have RBAC permissions       |



### Install plugins via krew

create a file plugin

```
cat > ~/plugins <<EOF
access-matrix
ca-cert
ctx
get-all
iexec
images
ns
pod-dive
pod-logs
whoami
who-can
EOF
```

Install the plugin with krew

```sh
for plugin in $(cat ~/plugin); do
echo -en $(kubectl krew install $plugin); done
```

Verify and list installed plugins

```sh
kubectl krew list
```

List plugin installed with `kubectl plugin`

```sh
kubectl plugin list
```

Output

````shell
controlplane $ kubectl krew list
PLUGIN         VERSION
access-matrix  v0.4.6
ca-cert        v0.0.0
ctx            v0.9.1
get-all        v1.3.6
iexec          v1.8.0
images         v0.3.2
krew           v0.3.4
ns             v0.9.1
pod-dive       v0.1.4
pod-logs       v1.0.1
who-can        v0.2.0
whoami         v0.0.35

controlplane $ kubectl plugin list
The following compatible plugins are available:

/root/.krew/bin/kubectl-access_matrix
/root/.krew/bin/kubectl-ca_cert
/root/.krew/bin/kubectl-ctx
/root/.krew/bin/kubectl-get_all
/root/.krew/bin/kubectl-iexec
/root/.krew/bin/kubectl-images
/root/.krew/bin/kubectl-krew
/root/.krew/bin/kubectl-ns
/root/.krew/bin/kubectl-pod_dive
/root/.krew/bin/kubectl-pod_logs
/root/.krew/bin/kubectl-who_can
/root/.krew/bin/kubectl-whoami
````



### kubectl plugins usage examples

```shell
kubectl whomai
```

Let's also look at the `who-can` plugin, which is equivalent to the `kubectl auth can-i VERB [TYPE/NAME]`:

```shell
kubectl who-can create nodes
```

Output

````shell
controlplane $ kubectl whoami
kubecfg:certauth:admin
controlplane $ kubectl who-can create nodes
No subjects found with permissions to create nodes assigned through RoleBindings

CLUSTERROLEBINDING                                    SUBJECT   	TYPE            SA-NAMESPACE
cluster-admin                                         system:masters   Group
permissive-binding                                    admin  		   User
permissive-binding                                    kubelet   	   User
permissive-binding                                    system:serviceaccounts   Group
system:controller:clusterrole-aggregation-controller  clusterrole-aggregation-controller  ServiceAccount  kube-system
controlplane $
````

**can-i**

```
controlplane $ kubectl auth can-i create pods
yes
controlplane $
```

who-can '*'

```shell
kubectl who-can '*' pods
```

Output

```
ontrolplane $ kubectl who-can '*' pods
No subjects found with permissions to * pods assigned through RoleBindings

CLUSTERROLEBINDING                                    SUBJECT   TYPE            SA-NAMESPACE
cluster-admin                                         system:masters   Group
permissive-binding                                    admin   User
permissive-binding                                    kubelet   User
permissive-binding                                    system:serviceaccounts   Group
system:controller:clusterrole-aggregation-controller  clusterrole-aggregation-controller  ServiceAccount  kube-system
controlplane $
```



Let's switch to one of the namespaces and run the `pod-dive` plugin command to get one of the pods:

```shell
controlplane $ kubectl ns
admins
dbadmins
default
developers
kube-node-lease
kube-public
kube-system

controlplane $ kubectl ns developers
Context "kubernetes-admin@kubernetes" modified.
Active namespace is "developers".
controlplane $ kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
frontend-deployment-78bb6679c6-256ln   1/1     Running   0          6m2s
frontend-deployment-78bb6679c6-qfrjt   1/1     Running   0          6m2s
frontend-deployment-78bb6679c6-vl7w8   1/1     Running   0          6m2s
controlplane $
```

Let's get the name of the first pod, assign it to a variable and run the `pod-dive` plugin:

```shell
POD=$(kubectl get pods -o=jsonpath='{.items[0].metadata.name}') && echo $POD
```

```shell
kubectl pod-dive $POD
```



Output

```shell
controlplane $ POD=$(kubectl get pods -o=jsonpath='{.items[0].metadata.name}') && echo$POD
frontend-deployment-78bb6679c6-256ln
controlplane $ kubectl pod-dive $POD
[node]      node01 [ready]
[namespace]  ├─┬ developers
[type]       │ └─┬ replicaset [deployment]
[workload]   │   └─┬ frontend-deployment-78bb6679c6 [3 replicas]
[pod]        │     └─┬ frontend-deployment-78bb6679c6-256ln [running]
[containers] │       └── nginx [0 restarts]
            ...
[siblings]   ├── haproxy-deployment-788ff46cb4-g4pch
             ├── haproxy-deployment-788ff46cb4-kv8ml
             ├── haproxy-deployment-788ff46cb4-n6gdj
             ├── db-deployment-86944b775-f8n4r
             ├── db-deployment-86944b775-mcjb8
             ├── db-deployment-86944b775-xzwm2
             ├── frontend-deployment-78bb6679c6-qfrjt
             ├── frontend-deployment-78bb6679c6-vl7w8
             ├── coredns-fb8b8dccf-66d69
             ├── katacoda-cloud-provider-d5df586b6-p5c7c
             ├── kube-keepalived-vip-lmks7
             ├── kube-proxy-m2k7b
             └── weave-net-dx6st

controlp
```

We can also display all the images in all namespaces:

```shell
kubectl images -A
```

Let's also explore the `access-matrix` plug-in, which is handy when looking for a RBAC Access matrix for Kubernetes resources:

```shell
kubectl access-matrix
```

Output

```
ontrolplane $ kubectl access-matrix
NAME                                                          LIST  CREATE  UPDATE  DELETE
apiservices.apiregistration.k8s.io                            ✔     ✔       ✔       ✔
bindings                                                            ✔
certificatesigningrequests.certificates.k8s.io                ✔     ✔       ✔       ✔
clusterrolebindings.rbac.authorization.k8s.io                 ✔     ✔       ✔       ✔
clusterroles.rbac.authorization.k8s.io                        ✔     ✔       ✔       ✔
componentstatuses                                             ✔
configmaps                                                    ✔     ✔       ✔       ✔
controllerrevisions.apps                                      ✔     ✔       ✔       ✔
cronjobs.batch                                                ✔     ✔       ✔       ✔
csidrivers.storage.k8s.io                                     ✔     ✔       ✔       ✔
csinodes.storage.k8s.io                                       ✔     ✔       ✔       ✔
customresourcedefinitions.apiextensions.k8s.io                ✔     ✔       ✔       ✔
daemonsets.apps                                               ✔     ✔       ✔       ✔
daemonsets.extensions                                         ✔     ✔       ✔       ✔
deployments.apps                                              ✔     ✔       ✔       ✔
deployments.extensions                                        ✔     ✔       ✔       ✔
endpoints                                                     ✔     ✔       ✔       ✔
events                                                        ✔     ✔       ✔       ✔
```

Lets revisit the context plugin with `kubectx` an alias for `kubect ctx`

```shell
kubectl ctx
```

In the intermediate scenario, we used the `kubectx` plugin, which is just an alias to the `kubectl ctx` command.

The non-plugin alternative is to run this command to switch between context:

```
kubectl config use-context CONTEXT_NAME
```



### Interacting with pods - kubectl logs

To dump logs from a specified pod or container into the standard output, use the `kubectl logs POD_NAME`

Let's switch to the kube-system namespace and access some logs:

```shell
kubectk ns kube-system
```

lets get all the pods

```
kubectl get pods
```

Use the pod-logs plugin to get the weave pods logs

```
kubectl pod-lods
```

Then, select from the list:

- The weave-net-xxxx pod
- The weave-npc container
- Review the logs

Alternatively, you can use the `kubectl logs POD_NAME -c CONTAINER_NAME` command as shown below:

```shell
kubectl logs weave-net-POD_NAME -C weave-npc
```

Switch back to the default namespace before moving on to the next step:

```shell
kubectl ns default
```

**Note:** *If the specific pod only has one container, then there is no need to add the `-c CONTAINER_NAME` option*

*lease also note that the `pod-logs` plug-in does not allow output redirection. Therefore, if you want to redirect the output use `kubectl logs` as such: `kubectl logs  weave-net-POD  -c weave-npc >~/weave.logs`*



### Interacting with pods - kubectl exec/iexec

Let's create a single container pod called `test` with an `nginx` image:

```shell
kubectl run test --image=nginx --restart=Never
```

Verify whether the `test` container is up and running:

```shell
kubectl get pods
```

Now let's get the output of the `date` command from the running `test` container without logging into it:

```shell
kubectl exec test date
```

Using the `iexec` plug-in, let's get the content of the `/etc/resolv.conf/` file from the running `test` container:

```shell
kubectl iexec test cat /etc/resolv.conf
```

To login and interact with the container's shell, type the below command:

```shell
kubectl iexec test
```

From the shell prompt, type the below command or copy/paste it into the shell:

```
echo  "Welcome to kubernetes!!">/tmp/welcome.txt
```

Check the contents of the file:

```
cat /tmp/welcome.txt
```

Type `exit` to exit the interactive shell.

Alternatively, you can use the below command

```
kubectl exec test -it --/bin/sh
```



### Interacting with Pods - kubectl cp

The `cp` command can be used to copy files and directories to and from containers within a pod.

Using the test `nginx` container pod we created in the previous step, let's copy the content of the `krew-install` directory to the test container's `/tmp` directory:

```shell
kubectl cp ~/krew-install test:/tmp
```

N**ote:** *If the pod has mutiple containers, then you need to add `-c CONTAINER_NAME` option. If the pod is in a different namespace, you can prefix the namespace name before the pod, as shown here: `kubectl cp namespace/pod-name:/dir`.*

Let's verify whether the directory has been copied. Enter the container's shell within the pod:

```
kubectl iexec test
```

List the content of the /tmp directory to verify if the directory has been copied:

```
ls /tmp/krew-install
```

Type `exit` to exit the shell.

Now, let's copy the welcome.txt file from the test container to the master server's /tmp directory:

```shell
kubectl cp test:tmp/welcome.txt /tmp
```

```shell
cat /tmp/welcome.txt
```

Clean Up

```
kubectl delete pods test
```



### Interacting with Nodes - kubectl taint

A taint consist of a key, value, and effect. As an argument, it is expressed as key=value:effect.

The effect should be of one these values: `NoShedule, PreferNoSchedule, or NoExecute`

Currently a taint can only be applied to a node, and when a node is tainted, no pods can be scheduled in it unless a PodSpec toleration matching the taint is added in the pod manifest file.

Here is how it is used with the `kubectl` command:

`kubectl taint NODE NAME KEY_1=VAL_1:TAINT_EFFECT`

```shell
kubectl get nodes
```

```
controlplane $ kubectl get nodes
NAME           STATUS   ROLES    AGE    VERSION
controlplane   Ready    master   3h4m   v1.14.0
node01         Ready    <none>   3h3m   v1.14.0
```

Let's taint `node01` as dedicated to the devops-group only:

```shell
kubectl taint node node01 dedicated=devops-groups:NoSchedule
```

Output

```shell
controlplane $ kubectl taint node node01 dedicated=devops-group:NoSchedule
node/node01 tainted
controlplane $
```

Verify that node01 is tainted

```shell
kubectl describe node node01 | grep -i taints
```

Check taints of all nodes

```shell
kubectl get nodes -o custom=columns=NAME:.metadata.name,TAINTS:.spec.taints[*].key
```

Deploy a single pod

```shell
kubectl run my-app --image=nginx --restart=Never
```

The newly deployed pod will be in a pending state, because it will not tolerate the taints applied to both nodes. Therefore, it will not be scheduled.

Let's show the pod:

```
kubectl get pod my-app
```

As you can see, the pod is in a pending state. The reason for that is the scheduler couldn't place it into any of the nodes, due to the taints applied to them. To see the error, type the below command and check under the events section:

```shell
kubectl describe pod my-app
```

or

```sh
kubectl get events
```



```
controlplane $ kubectl taint node node01 dedicate=devops-group:NoSchedule
node/node01 tainted
controlplane $ kubectl describe node node01 | grep -i taints
Taints:             dedicate=devops-group:NoSchedule
controlplane $ kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints[*].key
NAME           TAINTS
controlplane   node-role.kubernetes.io/master
node01         dedicate
controlplane $ kubectl run my-app --image=nginx --restart=Never
pod/my-app created
controlplane $ kubectl get pod my-app
NAME     READY   STATUS    RESTARTS   AGE
my-app   0/1     Pending   0          23s
controlplane $ kubectl describe pod my-app
Name:               my-app
Namespace:          kube-system
Priority:           0
PriorityClassName:  <none>
Node:               <none>
Labels:             run=my-app
Annotations:        <none>
Status:             Pending
IP:
Containers:
  my-app:
    Image:        nginx
    Port:         <none>
    Host Port:    <none>
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-bvj4s (ro)
Conditions:
  Type           Status
  PodScheduled   False
Volumes:
  default-token-bvj4s:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-bvj4s
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  38s (x2 over 38s)  default-scheduler  0/2 nodes are available: 2 node(s) had taints that the pod didn't tolerate.
controlplane $
```



There are 2 ways to solve this issue. We can add a toleration matching the taint that was applied to the nodes, or remove the taint from the nodes. 

For now, let's remove the taint on node01:

```shell
kubectl taint node node01 dedicate-
```

*Note: to remove a taint, append the `-` to the value of the key.*

```sh
ontrolplane $ kubectl taint node node01 dedicate-
node/node01 untainted
```

Once the taint is removed, the scheduler will place the pending pod into the untainted node in our case `node01`. Let's verify by running the below command:

```sh
kubectl get pod -o wide
```

```
 172.17.0.10   controlplane   <none>           <none>
my-app                                     1/1     Running            0          13m  10.44.0.2     node01         <none>           <none>
```



### Interacting with Nodes - Pod's tolerations

In this step, we have already created in the background a deployment manifest file and added some tolerations to the pods so they can be created or migrated onto the master node.

There are only two nodes (a control node, A.K.A master node, and a worker node) in this cluster. And by default, the control node is tainted with `node-role.kubernetes.io/master`, therefore, any pod that does not have a toleration matching the node's taint cannot be deployed onto the control node.

Let's now take a look at the deployment manifest file and check the added tolerations:

deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deploymentmetadata:
  name: nginx-deployment  labels:
    app: web    tier: frontend
  namespace: default
  spec:
  replicas: 4
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 80
      tolerations:
      - key: "node-role.kubernetes.io/master"
        operator: Exists
        effect: NoSchedule
```

Let's now take a look at the deployment manifest file and check the added tolerations:

```
cd ~/deployment && cat nginx-deployment.yaml | grep -A5 tolerations
```

We can deploy the manifest using either the `apply` or `create` command:

```shell
kubectl reate -f nginx-deployment.yaml
```

verify get pods

```
kubectl get pods
```

```
kubectl get pods -o wide
```

```shell
ontrolplane $ kubectl get pods -n default
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-dfffbfbd6-4tzw8   1/1     Running   0          4m5s
nginx-deployment-dfffbfbd6-dqnt7   1/1     Running   0          4m5s
nginx-deployment-dfffbfbd6-t7m5p   1/1     Running   0          4m5s
nginx-deployment-dfffbfbd6-vqzg5   1/1     Running   0          4m5s
controlplane $
```



### Interacting with Nodes- kubectl cordon

Let's now try to get the pods that are deployed on the master node and assign them to a variable:

```
POD_MASTER=$(kubectl get pods -o=jsonpath='{.items[?(@.spec.nodeName == "master")].metadata.name}')  && echo $POD_MASTER
```

Now, let's run the pod-dive plugin:

```
kubectl pod-dive $POD_MASTER
```

*This output shows a nice summary of the pod's resource tree.*

```sh
controlplane $ kubectl pod-dive my-app
[node]      node01 [ready]
[namespace]  ├─┬ kube-system
[type]       │ └─┬ pod
[workload]   │   └─┬ [no replica set]
[pod]        │     └─┬ my-app [running]
[containers] │       └── my-app [0 restarts]
            ...
[siblings]   ├── nginx-deployment-dfffbfbd6-dqnt7
             ├── nginx-deployment-dfffbfbd6-t7m5p
             ├── nginx-deployment-dfffbfbd6-vqzg5
             ├── coredns-fb8b8dccf-5cmvj
             ├── coredns-fb8b8dccf-6fh7s
             ├── katacoda-cloud-provider-7984859b89-n6xvj
             ├── kube-keepalived-vip-9thrf
             ├── kube-proxy-xggc8
             ├── test
             └── weave-net-zvp6n
```



Before we drain the node, we will `cordon` it first. `cordon` means ensuring that no pod can be scheduled on the particular node.

Lets go ahead and cordon node01

```sh
kubectl cordon node01
```

If you list the nodes now, you will find the status of `node01` set to `Ready,SchedulingDisabled`:

```sh
kubectl get nodes
```



### Interacting with Nodes - kubectl drain

Draining a node means removing all running pods from the node, typically performed for maintenance activities.

Open a second terminal (click the `+` button at the top of the terminal and select 'Open New Terminal') and run the below command to watch the output in **Terminal 2**:

```
watch -d kubectl get pods -o wide
```

Pay attention to the `NODE` column, which will show how the pods are migrating from `node01` to the `master` node.

Go back to **Terminal 1** by clicking the 'Terminal' tab at the top of the screen. Run the below command to drain `node01`:

```sh
kubectl drain nodes01 --ignore-daemonsets
```

In **Terminal 1**, you will observe the pods are being evicted, and in **Terminal 2**, you will observe, how the pods in node01 are being terminated and re-deployed on the `master` node.

All your pods are now running on the master node at this point. You can now perform whatever maintenance is required on `node01` and when done, you can `uncordon` it to make it schedulable once again.

Please keep **Terminal 2** open. Now, let's `uncordon` node01.

In **Terminal 1**, ensure that `node01` is still at `Ready,SchedulingDisabled` mode:

```
kubectl get nodes
```

Now, lets uncordon nodes01

```
kubectl uncordon node01
```

Verfiy the node01 is now in Ready state

```
kubectl get nodes
```



In **Terminal 2**, you will notice that the pods have not been moved back to `node01`. These Pods will not be rescheduled automatically to the new nodes.

To get some pods running on `node01`, let's try to scale up the deployment to 8 replicas.

In **Terminal 1**:

```
kubectl scale deployment/nginx-deployment --replicas=8
```

In **Terminal 2**, you will notice, some of the pods are now running on `node01`.

**Note:** *The `--ignore-daemonsets` flag in the `kubectl drain` command is required because DaemonSet pods are required to run on each node when deployed. This allows pods that are not part of a DaemonSet to be re-deployed on another available node*



### Interacting with Nodes/Pods - kubectl top

The `kubectl top` allows you to see the resource consumption for nodes or pods. However, in order to use the `top` command, we have to install a metrics server.

Let's install a metrics server pod. To begin, let's clone the git repos below:

```
git clone https://github.com/mbahvw/kubernetes-metrics-server.git
```

```she
kubectl apply -f kuberentes-metrics-server
```

```shell
kubectl get --raw /apis/metrics.k8s.io
```



Output

```
ntrolplane $ kubectl  get --raw /apis/metrics.k8s.io/
{"kind":"APIGroup","apiVersion":"v1","name":"metrics.k8s.io","versions":[{"groupVersion":"metrics.k8s.io/v1beta1","version":"v1beta1"}],"preferredVersion":{"groupVersion":"metrics.k8s.io/v1beta1","version":"v1beta1"}}
controlplane $
```

We need to give the metrics server a few minutes in order to collect data.

Let's get the CPU and memory utilization for all nodes in the cluster:

```sh
kubectl top nodes
```

Now, let's try to get the memory and CPU utilization of pods in all namespaces:

```sh
kubectl top pods --all-namespaces
```

We can also gather the metrics of all the pods in the kube-system namespace:

```sh
kubectl top pods -n kube-system
```