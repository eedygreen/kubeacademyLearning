Setting Up Workstation on Linux for Kubernetes workload

### Requirements

- [Docker Desktop/Engine for Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu)
- [Go](https://golang.org/doc/install)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)
- [Kustomize](https://github.com/kubernetes-sigs/kustomize/blob/master/docs/INSTALL.md)
- [Helm](https://helm.sh/docs/intro/install)
- [Skaffold](https://skaffold.dev/docs/install)

## Install Docker

[Docker Desktop/Engine for Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu)

| for other Os environment 

| [Docker Desktop/Engine for Mac](https://docs.docker.com/docker-for-mac/install) 

| [Docker Desktop/Engine for Windows](https://docs.docker.com/docker-for-windows/install)

## Kind

Kind required Go version 1.11+

**Install the Golang compiler** 

``sudo apt install gccgo-go``

**Install go**

```sudo apt install golang-go```

**Test Go for successful installation**

``` go version```

Write hello world program in go

```vim hello.go```

```
import "fmt"

func main() {
	fmt.Println("Hello, world")
}
```

```go run hello.go```

`GO111MODULE="on" go get sigs.k8s.io/kind@v0.9.0`

curl 

## Kubectl

```bash
sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg2 curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update

sudo apt-get install -y kubectl
```

or

```bash
sudo snap install kubectl --classic
```

## Kustomize

Install kustomize

```bash
GOBIN=$(pwd)/ GO111MODULE=on go get sigs.k8s.io/kustomize/kustomize/v3
```



## Helm

Install helm

``sudo snap install helm --classic``



## Skaffold

```bash
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
sudo install skaffold /usr/local/bin/
```

