# WAN 2.2 RunPod Deployment Guide

## 📋 Prerequisites

1. **Docker Desktop** installed and running
2. **Docker Hub account** (free at https://hub.docker.com)
3. **RunPod account** with API key (get from https://runpod.io/console/user/settings)

## 🚀 Step-by-Step Deployment

### Step 1: Build Docker Image

The Docker image is currently being built for you. Once complete, you'll see:

```
✅ Docker image built successfully!
```

### Step 2: Tag and Push to Docker Hub

Replace `YOUR_USERNAME` with your Docker Hub username:

```bash
# Tag the image
docker tag wan2-video-generation YOUR_USERNAME/wan2-video-generation:latest

# Login to Docker Hub
docker login

# Push the image
docker push YOUR_USERNAME/wan2-video-generation:latest
```

### Step 3: Create RunPod Template

1. Go to https://runpod.io/console/user/templates
2. Click **"New Template"**
3. Fill in the form:
   - **Template Name**: `wan2-video-generation`
   - **Container Image**: `YOUR_USERNAME/wan2-video-generation:latest`
   - **Docker Start Command**: `python wan2_handler.py`
   - **Container Disk**: `50 GB`
   - **Volume Disk**: `100 GB` 
   - **Volume Mount Path**: `/workspace`
   - **Expose HTTP Ports**: `8188`
   - **Environment Variables**:
     ```
     PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
     ```

### Step 4: Deploy Serverless Endpoint

1. Go to https://runpod.io/console/serverless/user/functions
2. Click **"New Endpoint"**
3. Configure:
   - **Endpoint Name**: `wan2-video-generation`
   - **Select Template**: Choose your `wan2-video-generation` template
   - **GPU Type**: **A100 80GB** (required for 14B models)
   - **Max Workers**: `3`
   - **Idle Timeout**: `5` seconds
   - **Active Workers**: `0-1`

### Step 5: Update Your App

Once deployed, you'll get an endpoint URL like:
```
https://api.runpod.ai/v2/abc123def456/runsync
```

Update your `.env` file:
```bash
VITE_RUNPOD_ENDPOINT=https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync
VITE_RUNPOD_API_KEY=your_runpod_api_key_here
```

## 🧪 Test Your Deployment

Test with curl:

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "A beautiful sunset over the ocean waves",
      "resolution": "720p",
      "num_frames": 90,
      "guidance_scale": 4.0
    }
  }'
```

## 💰 Cost Estimates

- **Cold Start**: ~30-60 seconds (model loading)
- **Generation Time**: ~60-120 seconds for 90 frames
- **Cost per Generation**: ~$0.05-0.15 depending on length

## 🔧 Troubleshooting

### Common Issues:

1. **"Out of Memory"**
   - Solution: Use A100 80GB GPU only
   - Reduce resolution to 480p if needed

2. **"Model Download Failed"**
   - Solution: Increase timeout settings
   - Check internet connection on RunPod

3. **"Generation Timeout"**
   - Solution: Reduce num_frames or num_inference_steps
   - Use lower resolution

4. **"Endpoint Not Found"**
   - Solution: Check endpoint URL format
   - Verify API key is correct

## 📞 Support

- **RunPod Issues**: https://docs.runpod.io
- **Model Issues**: Check HuggingFace model pages
- **ComfyUI Issues**: https://github.com/comfyanonymous/ComfyUI

## 🎯 Models Used

- **Text-to-Video**: [NSFW-API/NSFW_Wan_14b](https://huggingface.co/NSFW-API/NSFW_Wan_14b)
- **Image-to-Video**: [Wan-AI/Wan2.2-I2V-A14B](https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B)

Both models are automatically downloaded on first use.