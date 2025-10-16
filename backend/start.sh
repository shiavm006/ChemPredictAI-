#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create downloads directory for models if it doesn't exist
mkdir -p ~/Downloads/TrainedData

# Start the application
uvicorn main:app --host 0.0.0.0 --port $PORT
