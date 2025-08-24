FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    unzip \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install runpod requests pillow opencv-python-headless

# Clone ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /workspace/ComfyUI

# Install ComfyUI dependencies
WORKDIR /workspace/ComfyUI
RUN pip install -r requirements.txt

# Install custom nodes for Wan2.2 support
RUN cd custom_nodes && \
    git clone https://github.com/kijai/ComfyUI-WanVideo.git

# Install WanVideo dependencies
WORKDIR /workspace/ComfyUI/custom_nodes/ComfyUI-WanVideo
RUN pip install -r requirements.txt

# Create model directories
RUN mkdir -p /workspace/ComfyUI/models/diffusion_models && \
    mkdir -p /workspace/ComfyUI/models/text_encoders && \
    mkdir -p /workspace/ComfyUI/models/vae && \
    mkdir -p /workspace/ComfyUI/models/loras && \
    mkdir -p /workspace/ComfyUI/output

# Copy our handler
COPY wan2_handler.py /workspace/wan2_handler.py

# Set working directory back to workspace
WORKDIR /workspace

# Expose ComfyUI port
EXPOSE 8188

# Set environment variables
ENV PYTHONPATH="/workspace/ComfyUI:$PYTHONPATH"
ENV COMFYUI_MODEL_MEMORY_LIMIT=20000
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Start the handler
CMD ["python", "wan2_handler.py"]