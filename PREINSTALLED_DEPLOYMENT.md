# Pre-installed Docker Image Deployment

## 🚀 GitHub Actions Build (Recommended)

### Step 1: Upload to Your GitHub Repo
Upload these files to a `runpod-setup` folder in `karlasmar/goonhub`:

```
runpod-setup/
├── wan2_handler.py
├── workflow_t2v.json
├── workflow_i2v.json  
├── Dockerfile.preinstalled
├── .github/
│   └── workflows/
│       └── build-docker.yml
└── PREINSTALLED_DEPLOYMENT.md
```

### Step 2: Add Docker Hub Secret
1. Go to your GitHub repo settings
2. Secrets and variables → Actions → New repository secret
3. Name: `DOCKER_PASSWORD`
4. Value: Your Docker Hub password

### Step 3: Trigger Build
1. Push files to your `main` branch
2. GitHub Actions will automatically build and push to `mariogx/wan2-video-generation:latest`
3. Build takes ~30-45 minutes (downloads 20GB+ of models)

### Step 4: Create RunPod Template
**Container Image**: `mariogx/wan2-video-generation:latest`
**Container Start Command**: `python wan2_handler.py`

## ⚡ Benefits of Pre-installed Image

### Before (GitHub method):
- ❌ 5-10 minute cold start
- ❌ Downloads models every time
- ❌ Network dependent

### After (Pre-installed):
- ✅ 10-30 second cold start  
- ✅ All models pre-downloaded (~20GB)
- ✅ Everything ready to go

## 🎯 What's Pre-installed

### Models:
- `wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors` (7.5GB)
- `wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors` (7.5GB)
- `wan2.2_i2v_high_noise_14B_fp16.safetensors` (8.9GB)
- `wan2.2_i2v_low_noise_14B_fp16.safetensors` (8.9GB)
- `wan_2.1_vae.safetensors` (335MB)
- `umt5_xxl_fp8_e4m3fn_scaled.safetensors` (4.7GB)

### Software:
- ComfyUI with WanVideo nodes
- All Python dependencies
- System packages

## 💰 Cost Comparison

| Method | Cold Start | Monthly Cost* |
|--------|-----------|---------------|
| GitHub Method | 5-10 min | Higher (downloads) |
| Pre-installed | 10-30 sec | Lower (no downloads) |

*Based on A100 80GB usage

## 🔧 RunPod Template Settings

```yaml
Template Name: mario-wan2-preinstalled
Container Image: mariogx/wan2-video-generation:latest
Container Start Command: python wan2_handler.py
Container Disk: 50 GB
Volume Disk: 100 GB  
Volume Mount Path: /workspace
Expose HTTP Ports: 8188
Environment Variables:
  PYTORCH_CUDA_ALLOC_CONF: expandable_segments:True
```

## 🧪 Test Your Endpoint

Same API as before, but much faster response times!

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer rpa_UBJUKYG839LGMV2F3TPYFBTYNLVYW7I5NMB0V7YT1gdzhd" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "A beautiful sunset over ocean waves",
      "resolution": "720p",
      "num_frames": 90
    }
  }'
```