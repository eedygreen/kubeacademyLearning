# RBAC

**Role Based Access Control** (RBAC)

The subjects users perform operations on object using the role assigned to them.

**Sujects are;**

- Users

- Administrator

- Service Account

- Running Processes

**Operations**

- get

- delete

- create

- patch

- watch

**API Resources**

- pods

- Service

- deployment

- Secrete

- Configmap

- PVC

- Nodes

```shell
kubectl get role # display all roles

kubectl get role role_name # display this specific role

kubectl get role prometheus-k8s -o yaml
```

using the command `kubectl get role prometheus-k8s -o yaml` to display the config file, in the section rules

```yaml
kind: Role
```



```yaml
rules:
- apiGroups:
  - ""
  resources:				# resources
  - servicees
  - endpoints
  - pods
  verbs:					# operations
  - get
  - list
  - watch
```

the assigned API Resources and Operations for the Prometheus role also shows that this cannot delete any resources.

**RoleBinding**

The mapping of the role (Resources + Operations) to a subject (user, Service Account, Administrator, Running Processes) is called Role Binding.

```shell
kubectl get rolebinding		# display all role binding

kubectl get rolebinding rolebinding_name # display specific rolebinding

kubectl get rolebinding rolebinding_name -o yaml
```

Note: Kind will be assigned the resource type

```yaml
kind: RoleBinding
```

```yaml
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: prometheus-k8s
subjects:
- kind: ServiceAccount
  name: prometheus-k8s
  namespace: monitoring
```



To verify the service account in the namespace monitoring

```shell
kubectl get ServiceAccount -n monitoring
```



```shell
kubectl api-resources		# view all resources available
```

