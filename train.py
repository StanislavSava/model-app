import torch
import torch.nn as nn
import torch.optim as optim

device = (
    torch.device('mps') if torch.backends.mps.is_available() 
    else torch.device('cuda') if torch.cuda.is_available()
    else torch.device('cpu')
)

model = nn.Sequential(
    nn.Linear(200, 140),
    nn.ReLU(),  
    nn.Linear(140, 100),
    nn.ReLU(),  
    nn.Linear(100, 20),
    nn.ReLU(),  
    nn.Linear(20, 10),
    nn.ReLU(),  
    nn.Linear(10, 2)).to(device)

optimizer = optim.Adam(model.parameters(), lr=0.001)

loss_func = nn.CrossEntropyLoss()


x = torch.arange(0, 100000).reshape((500, 200)).float().to(device)
y = torch.arange(1, 501).reshape((500,)).float().to(device)

for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(x)
    loss = loss_func(outputs, y)
    loss.backward()
    optimizer.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

print(model(torch.arange(0, 200).reshape((200,)).float().to(device)))
