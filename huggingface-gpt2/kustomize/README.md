# Kubernetes Deployment using Kustomize for GPT-2 FastAPI App

This repository contains Kubernetes deployment configurations using Kustomize for a GPT-2 FastAPI application. It provides separate overlays for development and production environments.

## Usage
First make sure you have the required images on the minikube image registry. Use `minikube image list` and check if these two images are there:
```bash
docker.io/library/fastapi-mlflow-prod:v1
docker.io/library/fastapi-mlflow-dev:v1
```
If not use this command to build the images:
```bash
minikube image build -f Dockerfile_dev -t fastapi-mlflow-dev:v1 .
minikube image build -f Dockerfile_prod -t fastapi-mlflow-prod:v1 .
```
### Development Environment

To view the manifest files for the development environment:

```bash
kubectl kustomize overlays/dev | less
```

Alternatively, you can generate the manifest files and compare with the original file `gpt2_dev.yaml`
```bash
kubectl kustomize overlays/dev > kustomize_gpt2_dev.yaml
```

To deploy to the development environment:
```bash
kubectl apply -k overlays/dev
```

Access the API documentation in your browser at: http://local-server/fastapi/dev/docs

To stop and remove the application:
```bash
kubectl delete -k overlays/dev
```

### PRODUCTION ENVIRONMENT
To view the manifest files for the production environment:
```bash
kubectl kustomize overlays/prod | less
```

To generate the manifest files:

```bash
kubectl kustomize overlays/prod > kustomize_gpt2_prod.yaml
```

To deploy to the production environment:

```bash
kubectl apply -k overlays/prod
```

Access the API documentation in your browser at: http://local-server/fastapi/prod/docs

To stop and remove the application:
```bash
kubectl delete -k overlays/prod
```

Make sure your Kubernetes cluster and `mlflow-tracking-server` is up and running before applying these configurations.

Happy Continuous Learning!
