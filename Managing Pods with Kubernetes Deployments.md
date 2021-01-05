# Managing Pods with Kubernetes Deployments

**Deployment**

By editing the deployment file you eliminate the use of re-applying the deployment. As soon as the deployment is edited the changes is applied immediately without explicitly using `kubectl apply` . It does this through the label selector.

```shell
kubectl edit resource/name

kubectl edit deployment/quardi
```



**Pod**

Pod can be edited as well using the label selector

```shell
kubectl get pods  #get the name of running pods
```

editing a pod

```shell
kubectl edit pods pods-name
```

 *Note*

| Changing the image of a deployment or replica set will trigger a rolling deployment

Check replica set

```shell
kubectl get rs
```



**Rollback**

```shell
kubectl rollout undo deployment/qurdi
```



**Exposing Services**

- Using the Cluster Ip

```shell
kubectl get svc
```

Forward the Cluster IP address

```shell
kubectl port-forward service/name localport:nodeport

kubectl port-forward service/qurdi 9000:8080
```

- Using the Nodeport

```yaml
apiVersion: v1
kind: Service
metadata:
  name: building-apps-svc
  labels:
    app: kubeacademy
spec:
  selector:
    app: kubeacademy
    type: NodePort					#Specify type as NodePort
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

Every node on that cluster is reachable via the port chosen by the nodeport selector `kubectl get svc` will display the associated port.



User Service LoadBalancer

```yaml
apiVersion: v1
kind: Service
metadata:
  name: building-apps-svc
  labels:
    app: kubeacademy
spec:
  selector:
    app: kubeacademy
    type: LoadBalancer		# Specify type LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000

```

The LoadBalancer will expose the service to the cluster to be reachable from the outside.



**NameSpaces**

```shell
kubectl get ns
```

look into the namespaces, especially the kube-system

```shell
kubectl get po -n kube-system
```

The output should display some of the controllers, proxy and so on.

| Not all kubernetes application should be run as namespaces. The api command let you know which of the application can be run as namespace.

```shell
kubectl api-resources
```

Deleting a namespace will not delete resources not part of the namespace; persistent volume, nodeport...

```shell
kubectl delete -n dev
```

