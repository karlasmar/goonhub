#!/bin/bash

# RunPod Deployment Script for Wan 2.2 Video Generation
# This script builds and deploys the Docker container to RunPod

set -e

echo "🚀 Starting Wan 2.2 RunPod Deployment"

# Configuration
DOCKER_IMAGE_NAME="wan2-video-generation"
RUNPOD_TEMPLATE_NAME="wan2-comfyui-template"

# Check if required environment variables are set
if [ -z "$RUNPOD_API_KEY" ]; then
    echo "❌ RUNPOD_API_KEY environment variable is required"
    echo "   Set it with: export RUNPOD_API_KEY=your_api_key_here"
    exit 1
fi

echo "📦 Building Docker image..."
docker build -t $DOCKER_IMAGE_NAME .

echo "🏷️ Tagging image for registry..."
REGISTRY_IMAGE="mariogx/$DOCKER_IMAGE_NAME:latest"
docker tag $DOCKER_IMAGE_NAME $REGISTRY_IMAGE

echo "📤 Pushing to registry..."
docker push $REGISTRY_IMAGE

echo "🎯 Creating RunPod template..."
curl -X POST \
  https://api.runpod.ai/graphql \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { saveTemplate(input: { name: \"'$RUNPOD_TEMPLATE_NAME'\", imageName: \"'$REGISTRY_IMAGE'\", dockerStartCmd: \"python wan2_handler.py\", isRunpod: true, isPublic: false, readme: \"Wan 2.2 Video Generation with ComfyUI\", containerDiskInGb: 50, volumeInGb: 100, volumeMountPath: \"/workspace\", ports: \"8188/http\", env: [{ key: \"PYTORCH_CUDA_ALLOC_CONF\", value: \"expandable_segments:True\" }] }) { id name } }"
  }'

echo ""
echo "✅ Deployment complete!"
echo "🎬 Your Wan 2.2 video generation endpoint is ready"
echo ""
echo "📋 Next steps:"
echo "   1. Update your environment variables with the new endpoint URL"
echo "   2. Test the endpoint with a sample request"
echo "   3. Update your application to use the new Wan 2.2 models"
echo ""
echo "🔗 Models supported:"
echo "   • Text-to-Video: NSFW-API/NSFW_Wan_14b"
echo "   • Image-to-Video: Wan-AI/Wan2.2-I2V-A14B"