#!/bin/bash
# This script tests the Docker container locally

# Build the Docker image (replace with your actual HF token)
echo "Building Docker image..."
docker build --build-arg HF_TOKEN=your_huggingface_token -t eko-mistral-runpod:test .

# Run the Docker container
echo "Running Docker container..."
docker run -d --name eko-mistral-test -p 8000:8000 -p 8080:8080 eko-mistral-runpod:test

# Wait for the container to start
echo "Waiting for container to start..."
sleep 10

# Test the RunPod API
echo "Testing RunPod API..."
curl -X POST \
  http://localhost:8080/run \
  -H 'Content-Type: application/json' \
  -d '{
    "input": {
      "prompt": "What is climate change?"
    }
  }'

echo -e "\n\n"

# Test the OpenAI API - List models
echo "Testing OpenAI API - List models..."
curl http://localhost:8000/v1/models

echo -e "\n\n"

# Test the OpenAI API - Chat completion
echo "Testing OpenAI API - Chat completion..."
curl -X POST \
  http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "eko-mistral",
    "messages": [
      {"role": "system", "content": "You are a helpful AI assistant."},
      {"role": "user", "content": "What is climate change?"}
    ]
  }'

echo -e "\n\n"

# Clean up
echo "Cleaning up..."
docker stop eko-mistral-test
docker rm eko-mistral-test

echo "Tests complete!"