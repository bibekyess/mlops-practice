# Define base image
FROM python:3.11.4

# Install MLFlow
RUN pip install mlflow[extras]==2.5.0

# Expose MLFlow default port
EXPOSE 5000

# Run MLFLow server
ENTRYPOINT ["mlflow", "server", "--backend-store-uri", "sqlite:///mlflow.db", "--host", "0.0.0.0"]
