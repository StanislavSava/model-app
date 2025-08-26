import os
from huggingface_hub import InferenceClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

origins = ["*"]  # in prod, set this to your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model_url = os.environ.get("MODEL_URL", "http://llama-model:8080")

client = InferenceClient(
    model=model_url
)

class RequestModel(BaseModel):
    prompt: str

@app.post('/chat')
def chat(request: RequestModel):
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=100,
            temperature=0.7,
            top_p=0.95,
        )
    except Exception as e:
        print(f"Error during model inference: {e}")
        return {"error": str(e)}

    return {"response": response.choices[0].message.content}