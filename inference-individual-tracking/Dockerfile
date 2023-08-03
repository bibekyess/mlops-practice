FROM python:3.11.4

WORKDIR /app

COPY random_forest.py /app/random_forest.py

RUN pip install mlflow[extras]==2.5.0 scikit-learn

CMD ["python", "random_forest.py"]