# Deploying Application with Kustomize

Describe one or many context

```shell
kubectl config get-contexts
```



Use the watch command to get real-time view and avoid typing the get pod command after every deployment

```shell
watch kubectl get po
```





```shell
watch kubectl get svc
```



List a pod identified by type and name specified in "pod.yaml" in JSON output format.

```  shell
kubectl get -f pod.yaml -o json
```

 List resources from a directory with kustomization.yaml - e.g.
dir/kustomization.yaml.

 ```shell
kubectl get -k dir/

kubectl get -k base/		# where base is a directory
 ```



**Kustomize**

Kustomize introduces a template-free way to customize application configuration that simplifies the use of off-the-shelf applications. Now, built into `kubectl` as `apply -k`.

Kustomize traverses a Kubernetes manifest to add, remove or update configuration options without forking. It is available both as a standalone binary and as a native feature of `kubectl`.

```shell
kustomize build ~/someapp
```

The output can be passed as a standard input to kubectl

```shell
kustomizw build name/manifest.yaml | kubectl apply -f -
```



```
~/someApp
├── base
│   ├── deployment.yaml
│   ├── kustomization.yaml
│   └── service.yaml
└── overlays
    ├── development
    │   ├── cpu_count.yaml
    │   ├── kustomization.yaml
    │   └── replica_count.yaml
    └── production
        ├── cpu_count.yaml
        ├── kustomization.yaml
        └── replica_count.yaml
```

Kustomize generate a single yaml template that can be used to apply configuration management.