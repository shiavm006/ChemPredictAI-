FROM python:3.11-slim

WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# copy backend files
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY backend/ .

# expose port
EXPOSE 7860

# run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

