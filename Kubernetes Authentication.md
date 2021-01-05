# [Kubernetes Authentication](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#openid-connect-tokens)

There are three basic ways to authenticate with kubernetes, see the authentication strategies [link](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#authentication-strategies) 

- Certificate Authority
- IAM Authenticator
- Open ID Connect (OIDC)



**Certificate Authority**

openssl can be used to generate the certificate

Note: In the deployment file, under the 

```shell
openssl req -new -key jbeda.pem -out jbeda-csr.pem -subj "/CN=jbeda/O=app1/O=app2"
```

This would create a CSR for the username "jbeda", belonging to two groups, "app1" and "app2". [here](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#x509-client-certs)

```shell
spec:
	containers:
	- command:
	  - kube-apiserver
	  - --client-ca-file=/etc/kuberenetes/pki/ca.crt #specify the certificate 
```



**IAM Authenticator**

Configuration details [here](https://github.com/kubernetes-sigs/aws-iam-authenticator)

```shell
spec:
	containers:
	- command:
	  - kube-apiserver
	  - --authentication-token-webhook-config-file=/etc/kuberenetes/pki/aws-iam-authenticator/kubeconfig.yaml #specify the iam-authenticator 
```



**[OpenID Connect](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#openid-connect-tokens)**

There are three ways to implement OpenID Connect.

- UAA [User Account and Authentication Server](https://docs.cloudfoundry.org/concepts/architecture/uaa.html)

  "The primary role of UAA is as an OAuth2 provider, issuing tokens for client apps to use when they act on behalf of CF users. In collaboration with the login server, UAA can authenticate users with their CF credentials, and can act as an SSO service using those, or other, credentials."

- **Dex** [Kubernetes authentication through plugin](https://dexidp.io/docs/kubernetes/)

  Dex provide OpenID authentication through the use of connectors and it supports [LDAP](https://dexidp.io/docs/connectors/ldap/), [GitHub](https://dexidp.io/docs/connectors/github/), [SAML 2.0](https://dexidp.io/docs/connectors/saml/), [Gitlab](https://dexidp.io/docs/connectors/gitlab/), [OpenID Connect](https://dexidp.io/docs/connectors/oidc/), [Google](https://dexidp.io/docs/connectors/google/), [LinkedIn](https://dexidp.io/docs/connectors/linkedin/), [Microsoft](https://dexidp.io/docs/connectors/microsoft/), [AuthProxy](https://dexidp.io/docs/connectors/authproxy/), [Bitbucket Cloud](https://dexidp.io/docs/connectors/bitbucketcloud/), [OpenShift](https://dexidp.io/docs/connectors/openshift/), [Atlassian Crowd](https://dexidp.io/docs/connectors/atlassian-crowd/), [Gitea](https://dexidp.io/docs/connectors/gitea/), [Integration kubelogin and Active Directory](https://dexidp.io/docs/connectors/kubelogin-activedirectory/), 

  

- **OpenUniso**n [Tremelo Security](https://www.tremolosecurity.com/products/orchestra-for-kubernetes)

  The OpenUnison provide authentication solution for kubernetes and Openshift using Active Directory/LDAP, SAML 2.0, OpenID Connect and GitHub.

Dex Identity Provider, DexIDP, is a trusted centralize 

 Configuring the kubernetes with [dexidp.io](https://dexidp.io/docs/kubernetes/)

```shell
spec:
	containers:
	- command:
	  - kube-apiserver
	  - --client-ca-file=/etc/kuberenetes/pki/ca.crt #specify the certificate 
	   - --authentication-token-webhook-config-file=/etc/kuberenetes/pki/aws-iam-authenticator/kubeconfig.yaml #specify the iam-authenticator 
	   - --oidc-issuer-url=https://dex.k16opus.info/dex
	   - --oidc-client-id=gangway
	   - --oidc-username-claim=email
	   - --oidc-groups-claim=groups
```



### Gangway

The easiest way to implement the OpenID Connect (OIDC) is to use [gangway](https://github.com/heptiolabs/gangway). use the illustration of the [README](https://github.com/heptiolabs/gangway/blob/master/docs/dex.md) to configure ganway.

The API Server must be configured for OIDC

```shell
kube-apiserver
...
--oidc-issuer-url="https://example.auth0.com/"
--oidc-client-id=3YM4ue8MoXgBkvCIHh00000000000
--oidc-username-claim=email
--oidc-groups-claim=groups
```

**Requirements To Build Gangway**

Go version ~=1.12

[esc](https://github.com/mjibson/esc)

esc embeds file into go programs and provides http file system interfaces to them.

**Installation**

```shell
go get -u github.com.mjibson/esc
```

Build the gangway: use the command below

```shell
go get -u github.com/heptiolabs/gangway
cd $GOPATH/src/github.com/heptiolabs/gangway
make setup
make
```

Gangway can be connected to other three different Identity Provider, see the 

- Dex

- Google

- Auth0

### Deploying Gangway

Use the illustration in [github](Deploying Gangway)



export KUBECONFIG=kubeconfig-eedy-certs

