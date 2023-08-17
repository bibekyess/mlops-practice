# Helm Deployment for GPT-2 FastAPI App

This repository provides Helm charts for deploying a GPT-2 FastAPI application in Kubernetes. It includes separate configurations for development and production environments.

## Usage

### Development Environment

To view the manifest files in the development environment:

```bash
helm template dev-templ --values values.yaml -f values_dev.yaml . | less
```

Alternatively, you can generate the manifest files and compare with the original file `gpt2_dev.yaml`
```bash
helm template dev-templ --values values.yaml -f values_dev.yaml . > helm_gpt2_dev.yaml
```

To deploy to the development environment:
```bash
helm install gpt2-dev-release --values values.yaml -f values_dev.yaml .
```

Access the API documentation in your browser at: http://local-server/fastapi/dev/docs

To stop and remove the application:
```bash
helm uninstall gpt2-dev-release
```

### PRODUCTION ENVIRONMENT
To view the manifest files for the production environment:
```bash
helm template prod-templ --values values.yaml -f values_prod.yaml | less
```

To generate the manifest files:

```bash
helm template prod-templ --values values.yaml -f values_prod.yaml . > helm_gpt2_prod.yaml
```

To deploy to the production environment:

```bash
helm install gpt2-prod-release --values values.yaml -f values_prod.yaml .
```

Access the API documentation in your browser at: http://local-server/fastapi/prod/docs

To stop and remove the application:
```bash
helm uninstall gpt2-prod-release
```

To view the list of release charts:
```bash
helm list
```

Make sure your Kubernetes cluster and `mlflow-tracking-server` is up and running before applying these configurations.

Happy Continuous Learning!
