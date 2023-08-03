FROM python:3.11

COPY ./requirements.txt /webapp/requirements.txt

WORKDIR /webapp

RUN pip install -r requirements.txt

# RUN export ROOT_PATH="/fastapi"

COPY webapp/* /webapp/

ENTRYPOINT ["uvicorn"]

CMD ["--host", "0.0.0.0", "main:app", "--port", "8000"]