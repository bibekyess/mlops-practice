FROM python:3.11

COPY ./requirements.txt ./requirements.txt

WORKDIR .

RUN pip install -r requirements.txt

COPY ./mlflow_train.py ./mlflow_train.py

CMD ["python", "mlflow_train.py"]
