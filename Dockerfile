FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
