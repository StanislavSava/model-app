import torch
import torch.nn as nn
from fastapi import FastAPI



device = torch.device('cpu')

model = nn.Linear(10, 2).to(device)

model.load_state_dict(torch.load('model.pth', map_location=device))

model.eval()

app = FastAPI()

@app.get('/predict')
def predict(start: int = 1, end: int = 10):
    start = int(start)
    end = int(end)
    x = torch.randn(start, end).to(device)
    prediction = model(x)
    return {'prediction': prediction.argmax().item()}