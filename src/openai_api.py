from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import subprocess
import time
import uuid
import json
import os
from datetime import datetime

app = FastAPI(title="Eko Mistral OpenAI-compatible API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model definitions
class ModelData(BaseModel):
    id: str
    object: str = "model"
    created: int = int(time.time())
    owned_by: str = "organization-owner"

class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelData]

# Chat message schemas
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

class ChatCompletionChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage

# Formatter to convert messages to Ollama prompt format
def format_messages(messages: List[Message]) -> str:
    """
    Format messages according to the chat template expected by Mistral models.
    This may need to be adjusted based on the specific format your model expects.
    """
    # Create a single string prompt that Ollama can process
    formatted_messages = []
    
    for msg in messages:
        if msg.role == "system":
            formatted_messages.append(f"<|im_start|>system\n{msg.content}<|im_end|>")
        elif msg.role == "user":
            formatted_messages.append(f"<|im_start|>user\n{msg.content}<|im_end|>")
        elif msg.role == "assistant":
            formatted_messages.append(f"<|im_start|>assistant\n{msg.content}<|im_end|>")
    
    # Add the final assistant tag to prompt the model to generate a response
    formatted_messages.append("<|im_start|>assistant\n")
    
    # Join all messages with newlines
    return "\n".join(formatted_messages)

# Count tokens (very approximate)
def count_tokens(text: str) -> int:
    # Very simple approximation (1 token ~= 4 characters)
    return len(text) // 4

@app.get("/v1/models")
async def list_models():
    """List available models (OpenAI compatible endpoint)"""
    models = [
        ModelData(id="eko-mistral")
    ]
    return ModelList(data=models)

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    """Create a chat completion (OpenAI compatible endpoint)"""
    try:
        # Format messages for Ollama
        formatted_prompt = format_messages(request.messages)
        
        # Execute Ollama with the formatted prompt
        cmd = [
            "ollama", "run", "eko-mistral",
            "--temperature", str(request.temperature),
        ]
        
        # Add max_tokens if specified
        if request.max_tokens:
            cmd.extend(["--num-predict", str(request.max_tokens)])
        
        # Add the formatted prompt
        cmd.append(formatted_prompt)
        
        # Run Ollama
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Generate response
        model_output = result.stdout.strip()
        
        # Calculate token usage (approximate)
        prompt_tokens = count_tokens(formatted_prompt)
        completion_tokens = count_tokens(model_output)
        
        # Create response object
        return ChatCompletionResponse(
            id=f"chatcmpl-{str(uuid.uuid4())}",
            created=int(time.time()),
            model="eko-mistral",
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(role="assistant", content=model_output),
                    finish_reason="stop"
                )
            ],
            usage=ChatCompletionUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))