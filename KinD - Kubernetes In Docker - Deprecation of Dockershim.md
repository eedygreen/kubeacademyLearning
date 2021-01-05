KinD - Kubernetes In Docker - Deprecation of Dockershim

Kind uses the Containerd as the runtime but it also use docker for its build time. The quick guide [here](https://kind.sigs.k8s.io/docs/user/quick-start/#:~:text=kind%20runs%20a%20local%20Kubernetes,to%20run%20in%20a%20container.)



Installation 

[Here](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

Create Cluster

```sh
kind create cluster
```

This will create a single kubernetes cluster, pull the docker file and create the config file.

Get cluster

```shell
kind get cluster
```



This delete the cluster

```
kind delete cluster
```

Load image to cluster

```shell
kind load image docker-image my-image  #docker image
```

````shell 
kind load docker-image my-custom-image --name kind-2  # If using a named cluster you will need to specify the name of the cluster you wish to load the image into
````

```shell
kind load image-archive /my-image-archive.tar
```

```
docker build -t my-custom-image:unique-tag ./my-image-dir
kind load docker-image my-custom-image:unique-tag
kubectl apply -f my-manifest-using-my-image:unique-tag
```

Build Image

kind runs a local Kubernetes cluster by using Docker containers as “nodes”. kind uses the [`node-image`](https://kind.sigs.k8s.io/docs/design/node-image) to run Kubernetes artifacts, such as `kubeadm` or `kubelet`. The `node-image` in turn is built off the [`base-image`](https://kind.sigs.k8s.io/docs/design/base-image), which installs all the dependencies needed for Docker and Kubernetes to run in a container.

Currently, kind supports two different ways to build a `node-image` if you have the [Kubernetes](https://github.com/kubernetes/kubernetes) source in your host machine (`$GOPATH/src/k8s.io/kubernetes`), by using `docker` or `bazel`. To specify the build type use the flag `--type`. Note however that using `--type=bazel` on Windows or MacOS will not work currently due to Kubelet using [CGO](https://golang.org/cmd/cgo/) which requires GCC/glibc for linux. A workaround may be enabled in the future.

kind will default to using the build type `docker` if none is specified.

```
kind build node-image --type bazel
```

Create multiple cluster

## Advanced

### Configuring Your kind Cluster

For a sample kind configuration file see [kind-example-config](https://raw.githubusercontent.com/kubernetes-sigs/kind/master/site/content/docs/user/kind-example-config.yaml). To specify a configuration file when creating a cluster, use the `--config` flag:

```
kind create cluster --config kind-example-config.yaml
```

#### Multi-node clusters

In particular, many users may be interested in multi-node clusters. A simple configuration for this can be achieved with the following config file contents:

```yaml
# three node (two workers) cluster config
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
```

#### Control-plane HA

You can also have a cluster with multiple control-plane nodes:

```yaml
# a cluster with 3 control-plane nodes and 3 workers
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: control-plane
- role: control-plane
- role: worker
- role: worker
- role: worker
```

#### Mapping ports to the host machine

You can map extra ports from the nodes to the host machine with `extraPortMappings`:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    listenAddress: "0.0.0.0" # Optional, defaults to "0.0.0.0"
    protocol: udp # Optional, defaults to tcp
```

This can be useful if using `NodePort` services or daemonsets exposing host ports.

Note: binding the `listenAddress` to `127.0.0.1` may affect your ability to access the service.

#### Setting Kubernetes version

You can also set a specific Kubernetes version by setting the `node`'s container image. You can find available image tags on the [releases page](https://github.com/kubernetes-sigs/kind/releases). Please use the `sha256` shasum for your desired kubernetes version, as seen in this example:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  image: kindest/node:v1.16.4@sha256:b91a2c2317a000f3a783489dfb755064177dbc3a0b2f4147d50f04825d016f55
- role: worker
  image: kindest/node:v1.16.4@sha256:b91a2c2317a000f3a783489dfb755064177dbc3a0b2f4147d50f04825d016f55
```

### Enable Feature Gates in Your Cluster

Feature gates are a set of key=value pairs that describe alpha or experimental features. In order to enable a gate you have to [customize your kubeadm configuration](https://kubernetes.io/docs/setup/independent/control-plane-flags/), and it will depend on what gate and component you want to enable. An example kind config can be:

|                                                         COPY |
| -----------------------------------------------------------: |
| `kind: Cluster apiVersion: kind.x-k8s.io/v1alpha4 featureGates:  FeatureGateName: true` |

#### IPv6 clusters

You can run IPv6 single-stack clusters using `kind`, if the host that runs the docker containers support IPv6. Most operating systems / distros have IPv6 enabled by default, but you can check on Linux with the following command:

```sh
sudo sysctl net.ipv6.conf.all.disable_ipv6
```

You should see:

```sh
net.ipv6.conf.all.disable_ipv6 = 0
```

If you are using Docker on Windows or Mac, you will need to use an IPv4 port forward for the API Server from the host because IPv6 port forwards don't work on these platforms, you can do this with the following config:

```yaml
# an ipv6 cluster
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  ipFamily: ipv6
  apiServerAddress: 127.0.0.1
```

On Linux all you need is:

```yaml
# an ipv6 cluster
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  ipFamily: ipv6
```

### Configure kind to use a proxy

If you are running kind in an environment that requires a proxy, you may need to configure kind to use it.

You can configure kind to use a proxy using one or more of the following [environment variables](https://docs.docker.com/network/proxy/#use-environment-variables) (uppercase takes precedence):

- `HTTP_PROXY` or `http_proxy`
- `HTTPS_PROXY` or `https_proxy`
- `NO_PROXY` or `no_proxy`

> **NOTE**: If you set a proxy it would be passed along to everything in the kind nodes. `kind` will automatically append certain addresses into `NO_PROXY` before passing it to the nodes so that Kubernetes components connect to each other directly, but you may need to configure additional addresses depending on your usage.

### Exporting Cluster Logs

kind has the ability to export all kind related logs for you to explore. To export all logs from the default cluster (context name `kind`):

```
kind export logs
Exported logs to: /tmp/396758314
```

Like all other commands, if you want to perform the action on a cluster with a different context name use the `--name` flag.

As you can see, kind placed all the logs for the cluster `kind` in a temporary directory. If you want to specify a location then simply add the path to the directory after the command:

```
kind export logs ./somedir  
Exported logs to: ./somedir
```

The structure of the logs will look more or less like this:

```
.
├── docker-info.txt
└── kind-control-plane/
    ├── containers
    ├── docker.log
    ├── inspect.json
    ├── journal.log
    ├── kubelet.log
    ├── kubernetes-version.txt
    └── pods/
```

The logs contain information about the Docker host, the containers running kind, the Kubernetes cluster itself, etc.