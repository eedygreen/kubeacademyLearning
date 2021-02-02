# Kubernetes BackUp

The best tool for **BackUp**, **Clusters & Persistent Volume Migration**, **Disaster Recovery** is [**Velero**](https://velero.io/blog/velero-is-an-open-source-tool-to-back-up-and-migrate-kubernetes-clusters/)

**Installation**

use the container velero/velero:v1.5.2 or follow the github [repo](https://github.com/vmware-tanzu/velero/releases/tag/v1.5.2)

Here is a comprehensive page on how to install and use [velero](https://velero.io/docs/v1.5/)

```shell
kubectl get backups 		# it will return empy if there were no submitted backups
```

Create a namespace

```shell
kubectl create ns my-app			#my-app namespace
```

Deploy an application the my-backup-namespace

```shell
kubectl apply -f kuard.yaml -n my-app
```

Check deployment

```shell
kubectl get deploy -n my-app 
```

Create a Backup

```shell
velero backup create kuard-backup --selector app=kuard

 velero backup create kuard-backup --selector app=kuard -oyaml		# to view the backup settings before actually submitting it
 
 velero backup logs kuard-backup 	# to view the backup logs
 velero backup describe kuard-backup	# to view the  backup
```

Check the backup

```shell
kubectl get backups -n velero
```



check the desitnation

```shell
aws s3 ls velero-testing-bucket

aws s3 ls velero-testing-bucket/backup
```



**Disaster Recovery**

Delete the namespace - pods, services, deployment, nodes will be deleted

```shell
kubecctl delete ns my-app
```

verify the deletion

```shell
kubectl get ns				# my-app is not in the list
```



**Restore the Disaster from BackUp**

```shell
velero restore create --from-backup kuard-backup
```



```shell
kubectl get restore

kubectl get ns				# my-app namespace should be on list

kubectl get deploy -n my-app  # kuard app should be on ready and up to date
```

