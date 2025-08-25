import os
from huggingface_hub import InferenceClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

origins = ["*"]  # in prod, set this to your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model_url = os.environ.get("MODEL_URL", "http://model:80")

client = InferenceClient(
    model=model_url
)

@app.post('/chat')

def chat(prompt: str):
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7,
        top_p=0.95,
    )

    return response.choices[0].message.content