# Containers

Optimization Factors on why use containers

- Speed

- Consistency

- Governance

- Security

### Building a Container

```dockerfile
FROM golang
LABEL maintainer="edy@mail.com"
WORKDIR /workspace
COPY . .
RUN go install
ENTRYPOINT ['hello']		
CMD ['world']
```

ENTRYPOINT AND CMD are always use to run application. if ENTRYPOINT is not used CMD can do the same otherwise CMD provides argument to ENTRYPOINT. In this case, CMD provide 'world' to ENTRYPOINT 'hello'

### Dockerignore

Docker **build** is done by the docker-daemon. Ignoring some files will reduce sending unnecessary to docker-daemon

This can be verified by using the grep command 

```shell
docker build -t heptio hleo-img | grep sending
```

Add the names unecessary files to ignore in .dockerignore file

```dockerfile
.dockerignore
```



### Graceful Shutdown

Using Control+C to stop container will caused the system to send SIGTERM to the parent process. Using ENTRYPOINT [''sh'', "-c", "Hello \"${0} \${*}\""] in the dockerfile will cause the shell to be the parent process and consequently will not get a graceful shutdown.

Work Around

Include `exec`	in front of hello

ENTRYPOINT ["sh", "-c", "exec hello \"${0} \${*} ""]

verify this with the `ps` command, the hello will have the pid of 1.

```shell
ps 
```



For Specialised Applications that does not trap the signal use the tini

tini is the backward spelling of init. Is the specialised purosed build program to be pid 1.

### Use the Flag to specify tini

```shell
docker run --init -e TINI_KILL_PROCESS_GROUP=1
```

 ### For Kubernetes

```dockerfile
FROM golang
LABEL maintainer="edy@mail.com"
WORKDIR /workspace
COPY . .
RUN go install
RUN apt-get update
RUN apt-get install tini
ENTRYPOINT ["tini", "-g", "--", "sh", "-c", "hello \"${0} \${*}\""]		
CMD ['world']
```

-g flag ensure it send the signal to the group

tini will be parent to the shell and grand parent to hello.



### Layers/Caching

Docker keeps the changes and actions of every build as layers and keep track of the event as cache. This can be viewed using history.

```shell
history helo-img
```

The command runs from top to bottom and this means any changes done at certain point will be re-evaluated. In the above dockerfile, if the source ode changes, then, an update and re-install of tini will repeated. This will cause more memory usage and overhead, a waste of resources.

The dockerfile can be rewritten as this

```dockerfile
FROM golang
LABEL maintainer="edy@mail.com"
WORKDIR /workspace
RUN apt-get update && apt-get install -y --no-install-recommends tini=0.18* && rm -rf /var/lib/opt/lists/*
COPY go.mod go.sum ./
RUN go mod download -json
COPY hello-go .
RUN ago install
ENTRYPOINT ["tini", "-g", "--", "sh", "-c", "hello \"${0} \${*}\""]		
CMD ['world']
```



```shell
docker build . -t green --no-cache
```

 With the new dockerfile, if the source code is modified, the build process will start from COPY command and skip the previous.



### Runtime, Image Size and Inspect

Check the id of the container

```shell
docker run --rm --entrypoint /bin/sh hello-img -c "id"
```

The trade-off of having root user privilege in application image is that we are giving the elevated access should the container be compromised. 

To solve this issue, define the USER with uid before building the container.

```dockerfile
FROM golang
LABEL maintainer="edy@mail.com"
WORKDIR /workspace
RUN apt-get update && apt-get install -y --no-install-recommends tini=0.18* && rm -rf /var/lib/opt/lists/*
COPY go.mod go.sum ./
RUN go mod download -json
COPY hello-go .
RUN ago install
USER 1001
ENTRYPOINT ["tini", "-g", "--", "sh", "-c", "hello \"${0} \${*}\""]		
CMD ['world']
```

Build the image and verify the user

```shell
docker run --rm --entrypiont /bin/sh helo-img -c "id"
```



### Image Sizing

Build Time and Run Time are to be considered to image sizing.

```dockerfile
FROM golang AS build
LABEL maintainer="edy@mail.com"
WORKDIR /workspace
COPY go.mod go.sum ./
RUN go mod download -json
COPY hello-go .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \ go build -a -installsufix cgo -o hello

FROM scratch
COPY --from=build /workspace/hello/
USER 1001
ENTRYPOINT ["hello"]		
CMD ['world']
```

 The dockerfile is separated into two the build image and the run time. There is a performance trade-off because `scratch` does not add OS, utilities and therefore makes it difficult to debug.



### Inspect

```shell
docker inspect helo-img

docker inspect helo-img -f '{{json .}}' | jq keys

docker inspect helo-img -f '{{json .Config}}' | jq keys # this gets only the config section
```



### Inspect Image Layers with dive

```shell
dive hel0-img
```

**dive** is a powerful tool that allows you to toggle between each layers and displayed the changes.

the container id can be used also

```shell
dive container_id
```

Tab key can be used to navigate to right hand side to view the changes and on the left the layers. Navigate to right and Ctrl+u to view the changes and used the Tab to navigate to left, scroll through each layers to view changes.



### JIB - Java Application

Jib is an Open Source tool developed by Google in 2018 for packaging Java application into containers. It eliminate the complexity to manage docker images. Jib only delas with the run time image and lets maven takes care of the build image.

Benefits of Jib

Simple

- Does not require a Dockerfile
- Does not require having Docker Daemon or Docker CLI installed
- Integrated with Maven and Gradle via plugin.

Fast

- Optimizes for build speed (leverages layers in docker images).
- Optimizes for application startup.

Reproducible

- Same app + same build metadata :arrow_right: Identitical image every time.

**Jib on Maven**

Does not require Docker Daemon or CLI

```shell
# default image name is artifactid:$version

mvn compile com.google.cloud.tools:jib-maven-plugin:2.2.0:build -Dimages=$REG/$REPO/$IMG:$TAG
```

Require Docker Daemon or CLI

```shell
# default image name is artifactid:$version

mvn compile com.google.cloud.tools:jib-maven-plugin:2.2.0:dockerBuild [-Dimages=$IMG:$TAG]
```

Build as Tar

```shell
# default image name is artifactid:$version

mvn compile com.google.cloud.tools:jib-maven-plugin:2.2.0:buildTar

docker load --input target/jib-image.tar
```



Add Plugin to pom file

```xml
<plugin>
	<groupId>com.google.cloud.tools</groupId>
	<artifact>Id:jib-maven-plugins</artifact>
	<version>2.2.0</version>
	<configuration>
		<to>
			<image>$REG/$REPO/$IMG:$TAG</image>
		</to>
	</configuration>
</plugin>
```



```shell
mvn complie jb:build
```

```shell
mvn compile jib:dockerBuild
```

```shell
mvn compile jib:buildTar
```



To have a shell using Jib, introduce the debug in pom.xml

```xml
<plugin>
	<groupId>com.google.cloud.tools</groupId>
	<artifact>Id:jib-maven-plugins</artifact>
	<version>2.2.0</version>
	<configuration>
		<from>
			<image>gcr.io/distroless/java:debug</image>
		</from>
	</configuration>
</plugin>
```



```shel
docker run --entrypoint /busy/box/sh image_name
```



### Buildpacks

Buildpacks has a cli utility that can be used to build the container image. To install Buildpacks follow the documentation [here](https://buildpacks.io/docs/tools/pack/)

"Pack is a tool maintained by the Cloud Native Buildpacks project to support the use of buildpacks.

It enables the following functionality:

1. [`build`](https://buildpacks.io/docs/concepts/operations/build/) an application using buildpacks.
2. [`rebase`](https://buildpacks.io/docs/concepts/operations/rebase/) application images created using buildpacks.
3. Creation of various [components](https://buildpacks.io/docs/concepts/components/) used within the ecosystem.

Pack works as both a [Command Line Interface (CLI)](https://buildpacks.io/docs/tools/pack/#pack-cli) and a [Go library](https://buildpacks.io/docs/tools/pack/#go-library)." from the Buildpacks.io web page

```shell
sudo add-apt-repository ppa:cncf-buildpacks/pack-cli
sudo apt-get update
sudo apt-get install pack-cli
```

using brew to install pack

```shell
brew install buildpacks/tap/pack
```

It also has a container build tool on dockerhub

- `buildpacksio/pack:latest`

```
docker run \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $PWD:/workspace -w /workspace \
  buildpacksio/pack build <my-image> --builder <builder-image>
```

using Github Installation

```shell
(curl -sSL "https://github.com/buildpacks/pack/releases/download/v0.15.1/pack-v0.15.1-linux.tgz" | sudo tar -C /usr/local/bin/ --no-same-owner -xzv pack)
```

 Go Library Installation

```shell
go get -u github.com/buildpacks/pack 
```

go get -u github.com/buildpacks/pack 



**Pack Build**

In the working directory, set the base image required to build the container

```shell
pack set-default-builder gcr.io/paketo-buildpacks/builder:base
```

To build a image, the command follows as `pack build name_image`

```shell
pack build go-img
```

To inspect image

```shell
pack inspect-image go-img
```

**The User**

Paketo set the user to non-root-user as a default.  An advantage over docker build. Its also worth mentioning that the Buildpacks image can be build exactly the same from any part of the world using same source code.

inspect the user id

```shell
docker run --rm --entrypoint /bin/sh go-img -c "id"
```

**Inspect The Builder**

```shell
pack inspect builder
```

**Patching**

To patch an Os after a release is published, this can  be done using the YAML file with the `pack rebase` command.

```shell
pack rebase go-image --run-image gcr.io/paketo-buildpacks/builder/run:0.0.17-base-crb
```

Check the images and you find there is a new image created

```shell
docker images
```

Inspect the image corresponding to the new file system

```shell
catd <(docker inspect image_id) <(docker inspect go-image) | tail -n 20
```

**Custom BuildPack**

```
pack build go-img --buildpack from-builder --buildpack directory
```



### Spring Boot

Sping Boot version 2.33.0 has cloud native support for Java. Spring Boot uses Paketo by default and uses the artifact ID and Version to name the image.

```shell
./mvnw spring-boot:build-image -DskipTests
```



```shell
pack inspect-image hello-java:1.0.0 --bom | jq '.local[].name' -r
pack inspect-image hello-java:1.0.0 --bom | jq '.local[] select(.name==dependecies")' -r
```



### Kpack

Kpack operates as a service in kubernetes and can be configured declaratively.



```shell
kubectl api-resources --api-group build.pivotal.io
```



kpack/builder.yaml

```yaml
apiVersion: build.pivotal.io/v1alpha1
kind: Builder
metadata:
	name: paketo-builder
spec:
	image: gcr.io/paketo-buildpacks/builder:base
```



kpack/image.yaml

```yaml
apiVersion: build.pivotal.io/v1alpha1
kind: Image
metadata:
	name: hello-go
spect:
	builder:
		name: paketo-builder
		kind: Builder
	serviceAccount: kpack-service-account
	cacheSize: "1.5Gi"
	source:
	 	git:
	 		url: https://github.om/cibrerkleid/hello-go
	 		revision: master
	 	subPath: src
	 tag: ciberkleid/hello-go:latest
```

Trigger on git source will cause the kpack to build the image

use the kubectl describe command to view the image

```shell
kubectl describe image hello-go
```



```shell
kubectl get build #LAST_BUILD -o json | jq .metadata.annotations
```



kpack logs

```shell
logs -namespace kpack-builds -image hello-go
```

