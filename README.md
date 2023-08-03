# MLops Practice

This repository contains learning materials for MLFlow, Docker, and Kubernetes.

## Docker Image Build and Push
If you don't want to build and push the new image, you can use my created image: `bibekyess/mlops-practice-mlflow:v1`
```bash
# Build the Docker image
docker build -t mlops-practice/mlflow-server .

# Tag the Docker image with your repository details
docker tag mlops-practice/mlflow-server:latest docker-hub-username/repo-name:tag

# Push the Docker image to Docker Hub
docker push docker-hub-username/repo-name:tag
```
## Kubernetes Deployment

```bash
# Go inside the configs folder
# Create the PersistentVolume(PV) and PersistentVolumeChain(PVC)
kubectl apply -f mlflow-pv.yaml
kubectl apply -f mlflow-pvc.yaml

# Deploy the MLFLow server using Deployment and Service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Enable Ingress for external access and create Ingress resource
minikube addons enable ingress
kubectl apply -f ingress.yaml
```
```bash
# Another alternative to do quickly is:
minikube addons enable ingress
kubectl apply -f . # If you are inside configs folder
kubectl apply -f configs # If you are on the root directory
```
```bash
# Get the MInikube IP and edit the host file for custom domain:
minikube ip # Copy to Clipboard
sudo nano /etc/hosts
# Add the following line at the end of the file:
# <Minikube-IP> local-server
```
Visit http://local-server in your web browser, and you will have the MLflow server running on the Kubernetes cluster.


Instead of pulling the image from the docker hub, you can instead load the docker image in the minikube docker daemon and then run container from there. `mlflow-server.yaml` contains the code for that and to run this:
```bash
minikube image load image-name:tag
minikube image list # Make sure you see docker.io/image-name:tag in here
kubectl apply -f mlflow-server.yaml
```