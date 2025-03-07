FROM runpod/base:0.4.0-cuda11.8.0

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install runpod huggingface_hub requests

# Set model constants
ENV MODEL_REPO="neileko/eko-mistral-small" \
    MODEL_PATH="/workspace/model"

# Download the model during build time
RUN mkdir -p ${MODEL_PATH} && \
    python -c "from huggingface_hub import snapshot_download; \
    snapshot_download(repo_id='${MODEL_REPO}', local_dir='${MODEL_PATH}', local_dir_use_symlinks=False)"

# Setup Ollama with the model
RUN mkdir -p /root/.ollama && \
    ollama serve > /dev/null 2>&1 & \
    sleep 5 && \
    ollama create eko-mistral -f ${MODEL_PATH}/Modelfile && \
    pkill ollama

# Copy the handler code
WORKDIR /app
COPY src/handler.py /app/handler.py

# Set the entrypoint
CMD ["python", "-u", "handler.py"]