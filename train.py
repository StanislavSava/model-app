import torch
import torch.nn as nn
import torch.optim as optim

device = (
    torch.device('mps') if torch.backends.mps.is_available() 
    else torch.device('cuda') if torch.cuda.is_available()
    else torch.device('cpu')
)

model = nn.Linear(10, 2).to(device)

optimizer = optim.Adam(model.parameters(), lr=0.001)

loss_func = nn.CrossEntropyLoss()


x = torch.randn(100, 10).to(device)
y = torch.randint(0, 2, (100,)).to(device)

for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(x)
    loss = loss_func(outputs, y)
    loss.backward()
    optimizer.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')


torch.save(model.state_dict(), 'model.pth')
