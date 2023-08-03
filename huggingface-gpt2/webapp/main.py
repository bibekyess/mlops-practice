from transformers import pipeline
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import mlflow
# import os

mlflow.set_tracking_uri("http://local-server")

generator = pipeline('text-generation', model='gpt2')

# app = FastAPI(root_path=os.getenv('ROOT_PATH', ''))
app = FastAPI(root_path='/fastapi')

class Body(BaseModel):
    text: str

@app.get("/")
def root():
    return HTMLResponse("<h1>API to interact with GPT2 and generate text</h1>")

@app.post('/generate')
def predict(body: Body):

    with mlflow.start_run():
        mlflow.log_param("input_prompt", body.text)

        results = generator(body.text, max_length=50, num_return_sequences=1)
        generated_text = results[0]['generated_text']

        mlflow.log_text(generated_text, 'generated_text')
        mlflow.log_metric('generated_text_length', len(generated_text))

        return {'generated_text', generated_text}
