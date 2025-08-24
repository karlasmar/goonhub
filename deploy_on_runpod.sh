#!/bin/bash
set -e

echo "🚀 Setting up WAN 2.2 Video Generation on RunPod"

# Install system dependencies
echo "📦 Installing system dependencies..."
apt-get update && apt-get install -y --no-install-recommends \
    git wget curl unzip ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --no-cache-dir runpod requests pillow opencv-python-headless

# Clone ComfyUI
echo "📥 Cloning ComfyUI..."
if [ ! -d "/workspace/ComfyUI" ]; then
    git clone https://github.com/comfyanonymous/ComfyUI.git /workspace/ComfyUI
fi

# Install ComfyUI dependencies
echo "🔧 Installing ComfyUI dependencies..."
cd /workspace/ComfyUI
pip install --no-cache-dir -r requirements.txt

# Install WanVideo custom node
echo "🎥 Installing WanVideo ComfyUI node..."
mkdir -p custom_nodes
cd custom_nodes
if [ ! -d "ComfyUI-WanVideo" ]; then
    git clone https://github.com/kijai/ComfyUI-WanVideo.git
fi
cd ComfyUI-WanVideo
pip install --no-cache-dir -r requirements.txt

# Create model directories
echo "📁 Creating model directories..."
mkdir -p /workspace/ComfyUI/models/diffusion_models
mkdir -p /workspace/ComfyUI/models/text_encoders
mkdir -p /workspace/ComfyUI/models/vae
mkdir -p /workspace/ComfyUI/output

# Copy our handler to the right location
echo "📋 Setting up WAN 2.2 handler..."
cp /workspace/setup/wan2_handler.py /workspace/wan2_handler.py

# Set environment variables
export PYTHONPATH="/workspace/ComfyUI:$PYTHONPATH"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

echo "✅ Setup complete! Starting WAN 2.2 handler..."

# Start the handler
cd /workspace
python wan2_handler.py