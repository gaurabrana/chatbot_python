#!/bin/bash

# Ensure required Python packages are installed
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install Python dependencies."
    exit 1
fi

# Define model path and URL
MODEL_PATH="./mistral-7b-instruct-v0.1.Q4_K_M.gguf"
MODEL_URL="https://huggingface.co/mistralai/mistral-7b-instruct-v0.1/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

# Check if model file exists
if [ -f "$MODEL_PATH" ]; then
    echo "Model already exists at $MODEL_PATH. Skipping download."
else
    echo "Downloading the model..."
    curl -L -o "$MODEL_PATH" "$MODEL_URL"
    
    if [ $? -ne 0 ]; then
        echo "Model download failed. Please check your internet connection or the URL."
        exit 1
    fi

    echo "Model downloaded successfully to $MODEL_PATH"
fi
