# Helm

Helm is a package manager for kubernetes clusters.

Helm chat is the directory where the helm manifest are stored.

Create a starting point for chart

```shell
helm create build4kube
```

 Use tree to look at the directory created

```shell
tree build4kube
```

```
tree build4kube/
build4kube/
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml

3 directories, 10 files
```

Note: You an remove the unnecessary files and leave the ones in need.



you can copy all the manifest into the template folder

```shell
cp deployment.yaml service.yaml /build4kube/template
```

**Deployment file**

Its important to exclude hard coded values to our files. Lets examine the deployment file.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: building-apps-deploy #values
  labels:
    app: kubeacademy
spec:
  replicas: 2  #values
  selector:
    matchLabels:
      app: kubeacademy
  template:
    metadata:
      labels:
        app: kubeacademy
    spec:
      containers:
      - name: building-apps-container
        image: lander2k2/building-apps:0.1  #values
```

The values can be changed to variables and this will removed the use of hardcoded values



```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: "{{ .Release.Name }}-building-apps-deploy"
  labels:
    app: kubeacademy
spec:
  replicas: {{ .Values.deploy.replicas }}
  selector:
    matchLabels:
      app: kubeacademy
  template:
    metadata:
      labels:
        app: kubeacademy
    spec:
      containers:
      - name: building-apps-container
        image: {{ .Values.deploy.image.repository }}:{{ .Chart.AppVersion }}

```



***Variable 1***: Every release will have an associated name with the .Release.Name function.

```yaml
"{{ .Release.Name }}-building-apps-deploy"
```



***Variable 2***: This variable will get the replica set values.

```yaml
{{ .Values.deploy.replicas }}
```



***Variable 3***: The first part of the variable `{{ .Values.deploy.image.repository }}`  will get the repository name and the other part separated with colon (:) will get the version of the of the application `{{ .Chart.AppVersion }}`

```yaml
{{ .Values.deploy.image.repository }}:{{ .Chart.AppVersion }}
```



**Service file**

Same can be done for any other files that has hard coded values

```yaml
apiVersion: v1
kind: Service
metadata:
  name: building-apps-svc  # values
  labels:
    app: kubeacademy
spec:
  selector:
    app: kubeacademy
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

 This can be modified as 

```yaml
apiVersion: v1
kind: Service
metadata:
  name: "{{ .Release.Name }}-building-apps-svc"
  labels:
    app: kubeacademy
spec:
  selector:
    app: kubeacademy
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```



These variables takes update from the values.yaml file in the helm chart directory. You can remove the default value file and create a new one or modified the original one. Better to create a new one.

```yaml
Deploy:
	replica:2
	image:
		repository: lander2k2/building-apps
```



Execute the following command outside the helm chart directory

```shell
helm install --generate-name /build4kube --dry-run
```

*Note*: helm install uploads the chart to **kubernetes**

Using the flag --dry-run will display the file that should have applied.

**Install helm chart**

To install the helm chart simply remove the flag --dry-run

```shell
helm install --generate-name /build4kube
```



**Upgrade**

To upgrade an application after change

```shell
sudo vim build4kube/chart.yaml
```

edit the **appVersion: values**, e.g appVersion: 0.1, save the changes and execute the command

```shell
helm upgrade build4kube-1606219407 ./build4kube
```

Check the update

```shell
kubectl get pods
```



```shell
kubectl desribe deploy pods-id-from-get-pods
```



**Rollback**

To rollback to previous services `helm rollback release-name`. This will undo the last upgrade done.

```shell
helm rollback build4kube-1606219407
```

 Check the Rollback

```shell
kubectl get all

kubectl describe deploy build4kube-1606219407-building-app-deploy
```

*Note*: The helm chart is not updated with the rollback. The appVersion is still as it was with the upgrade. This can be changed manually. 



**Helm package**

The helm package create a tar compressed file with the version number from the chart file.

```shell
helm package ./buid4kube
```

