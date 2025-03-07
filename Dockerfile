FROM runpod/base:0.4.0-cuda11.8.0

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install runpod huggingface_hub

# Copy the handler code
WORKDIR /app
COPY src/handler.py /app/handler.py

# Set the entrypoint
CMD ["python", "-u", "handler.py"]