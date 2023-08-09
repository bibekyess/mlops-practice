# Helm Chart for Web Application

This repository contains a Helm chart for deploying a web application using Kubernetes and Helm.

## Getting Started

To create the Helm chart, start by running the command:

```bash
helm create webapp1
```
It will generate a folder named webapp1 with several subfolders. The original contents are deleted and modified as in this github repo.

To deploy the application, follow the instructions below:

Clone this repository to your local machine.

Create the required namespaces:

```bash
kubectl create namespace dev
kubectl create namespace prod
```

To run the application in development:
```bash
helm install mywebapp-release-dev . --values values.yaml -f values_dev.yaml -n dev
```
To run the application in production:
```bash
helm install mywebapp-release-prod . --values values.yaml -f values_prod.yaml -n prod
```

If you make any changes to the application or its configurations, you can use the following command to upgrade the Helm release:
```bash
helm upgrade <release-name> . --values <values-filename>.yaml -n <namespace-name>
```
To view the application using port-forwarding
```bash
kubectl port-forward service/<service-name> 8888:80 --namespace <namespace-name>
```


### REFERENCES
https://github.com/devopsjourney1/helm-webapp/tree/main
