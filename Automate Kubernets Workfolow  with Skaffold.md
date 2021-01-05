# Improve Application Development with Skaffold


Fast. Repeatable. Simple.

Local Kubernetes Development.

[Get Skaffold ](https://skaffold.dev/docs/install/)

[Get Started ](https://skaffold.dev/docs/quickstart/)

Skaffold handles the workflow for building, pushing and deploying your application, allowing you to focus on what matters most: **writing code**.

The directory lesson 7

```yaml
tree
.
├── k8s
│   ├── deployment.yaml
│   └── service.yaml
├── README.md
└── src
    ├── Dockerfile
    └── main.go

2 directories, 5 files
```



**skaffold init**

To generate skaffold file use the `skaffold init`

```shell
skaffold init
```

 The `skaffold init` will create configuration skaffold.yaml file. The flag --force should be used in the place the configuration file already exist. The --force will override the previous configuration. The output of the initialization.

```yaml
ThinkPad-Edge-E431:~/Documents/KubeAcademy/building-apps-for-k8s-master/lesson-7]$ skaffold init
using non standard workspace: src
apiVersion: skaffold/v2beta9
kind: Config
metadata:
  name: lesson--
build:
  artifacts:
  - image: my-cool-app
    context: src
deploy:
  kubectl:
    manifests:
    - k8s/deployment.yaml
    - k8s/service.yaml

Do you want to write this configuration to skaffold.yaml? [y/n]: y
Configuration skaffold.yaml was written
You can now run [skaffold build] to build the artifacts
or [skaffold run] to build and deploy
or [skaffold dev] to enter development mode, with auto-redeploy
```



Run the `kubectl config current-context` to determine the kubernetes cluster that is running

*Note* 

| Skaffold should be execute in a directory with the kubernetes |manifest files; Dockerfile, Deployment.yaml, service.yaml 

**Skaffold build** : This will build the artifact

```shell
skaffold build
```

**Skaffold run**: This will build and deploy

```shell
skaffold run
```

**skaffold dev**: This will enter the development mode

```shel
skaffold dev
```



|Skaffold tag every build and uses the build to deploy the new changes. It also stream logs and watch for changes. Every change in code triggers skaffold while running the skaffold dev command and it instantly apply the changes. Its capable to detect manifest from code.

