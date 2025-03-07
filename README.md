# Eko Mistral RunPod Serverless

A RunPod serverless endpoint for running the Eko Mistral model using Ollama.

## Overview

This project sets up a RunPod serverless endpoint that:

1. Downloads the Eko Mistral model from HuggingFace (`neileko/eko-mistral-small`)
2. Sets up Ollama with the model using the provided Modelfile
3. Exposes an API endpoint to run inference with the model

## Deployment

### Prerequisites

- A RunPod account
- Docker installed locally (for building and testing)

### Building the Container

You'll need a Hugging Face token to download the model. You can generate one at https://huggingface.co/settings/tokens.

```bash
# Build with HF_TOKEN as a build argument
docker build --build-arg HF_TOKEN=your_huggingface_token -t your-dockerhub-username/eko-mistral-runpod:latest .
docker push your-dockerhub-username/eko-mistral-runpod:latest
```

> **Important**: Never commit your Hugging Face token to version control. When building in CI/CD environments, use secrets management.

### Deploying to RunPod

1. Navigate to the RunPod serverless dashboard: https://www.runpod.io/console/serverless
2. Click "New Endpoint"
3. Select a name and the GPU type
4. Enter your Docker image URL (e.g., `your-dockerhub-username/eko-mistral-runpod:latest`)
5. Configure any advanced settings as needed
6. Click "Deploy"

## Usage

### Standard RunPod API

Once deployed, you can send requests to your RunPod endpoint:

```bash
curl -X POST \
  https://api.runpod.ai/v2/your-endpoint-id/run \
  -H 'Content-Type: application/json' \
  -d '{
    "input": {
      "prompt": "What is climate change?"
    }
  }'
```

### OpenAI-Compatible API

The endpoint also exposes an OpenAI-compatible API that can be used with any OpenAI client library:

```bash
# List models
curl http://localhost:8000/v1/models

# Create a chat completion
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
```

#### Using with OpenAI Python Client

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1/",  # Replace with your RunPod URL
    api_key="not-needed"  # API key is not checked but required by the client
)

response = client.chat.completions.create(
    model="eko-mistral",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is climate change?"}
    ]
)

print(response.choices[0].message.content)
```

## Local Testing

To test locally:

```bash
# Build with your HF token
docker build --build-arg HF_TOKEN=your_huggingface_token -t eko-mistral-runpod:local .
docker run -p 8000:8000 -p 8080:8080 eko-mistral-runpod:local
```

Then send requests to:

### Test Standard RunPod API

```bash
python test.py --url http://localhost:8080/run --prompt "What is climate change?"
```

### Test OpenAI-Compatible API

```bash
python test_openai.py --url http://localhost:8000 --prompt "What is climate change?"
```