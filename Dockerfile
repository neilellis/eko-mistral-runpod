FROM runpod/base:0.4.0-cuda11.8.0

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Set model constants
ENV MODEL_REPO="neileko/eko-mistral-small" \
    MODEL_PATH="/workspace/model"

# ARG for HuggingFace token (to be passed at build time)
ARG HF_TOKEN

# Download the model during build time using token
RUN mkdir -p ${MODEL_PATH} && \
    python -c "from huggingface_hub import snapshot_download; \
    snapshot_download(repo_id='${MODEL_REPO}', local_dir='${MODEL_PATH}', \
    local_dir_use_symlinks=False, token='${HF_TOKEN}')"

# Setup Ollama with the model
RUN mkdir -p /root/.ollama && \
    ollama serve > /dev/null 2>&1 & \
    sleep 5 && \
    ollama create eko-mistral -f ${MODEL_PATH}/Modelfile && \
    pkill ollama

# Copy the handler code
WORKDIR /app
COPY src/handler.py /app/handler.py
COPY src/openai_api.py /app/openai_api.py

# Set the entrypoint
CMD ["python", "-u", "handler.py"]