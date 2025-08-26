FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy Python dependencies first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python application
COPY . .

# Expose port for FastAPI
EXPOSE 80

# Start your FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "./"]
