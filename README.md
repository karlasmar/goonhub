# Wan 2.2 Video Generation - RunPod Serverless

This RunPod serverless deployment provides state-of-the-art video generation using Wan 2.2 models with ComfyUI backend.

## Features

- **Text-to-Video**: Generate videos from text descriptions using `NSFW-API/NSFW_Wan_14b`
- **Image-to-Video**: Animate images using `Wan-AI/Wan2.2-I2V-A14B`
- **High Quality**: 14B parameter models for superior results
- **Flexible Resolutions**: 480p, 720p, and 1080p support
- **Advanced Controls**: CFG scale, sampling steps, motion strength, and more

## Models

### Text-to-Video (T2V)
- **Repository**: [NSFW-API/NSFW_Wan_14b](https://huggingface.co/NSFW-API/NSFW_Wan_14b)
- **Model Files**:
  - `wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors`
  - `wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors`

### Image-to-Video (I2V)
- **Repository**: [Wan-AI/Wan2.2-I2V-A14B](https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B)
- **Model Files**:
  - `wan2.2_i2v_high_noise_14B_fp16.safetensors`
  - `wan2.2_i2v_low_noise_14B_fp16.safetensors`

### Shared Components
- **VAE**: `wan_2.1_vae.safetensors`
- **Text Encoder**: `umt5_xxl_fp8_e4m3fn_scaled.safetensors`

## API Usage

### Text-to-Video Generation

```json
{
  "input": {
    "prompt": "A beautiful sunset over ocean waves, cinematic lighting",
    "negative_prompt": "blurry, bad quality, distortion",
    "guidance_scale": 4.0,
    "num_inference_steps": 30,
    "resolution": "720p",
    "num_frames": 90,
    "fps": 24,
    "motion_strength": 7,
    "sample_shift": 8,
    "seed": -1
  }
}
```

### Image-to-Video Generation

```json
{
  "input": {
    "image_url": "https://example.com/image.jpg",
    "prompt": "animate this image with smooth motion",
    "negative_prompt": "camera shake, distortion",
    "guidance_scale": 4.0,
    "num_inference_steps": 30,
    "resolution": "720p",
    "num_frames": 90,
    "fps": 24,
    "motion_strength": 7,
    "sample_shift": 8,
    "seed": -1
  }
}
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | required | Text description of the video |
| `negative_prompt` | string | auto | What to avoid in generation |
| `image_url` | string | optional | URL for I2V mode (if provided, switches to I2V) |
| `guidance_scale` | float | 4.0 | CFG scale (1-8, lower = less overcooked) |
| `num_inference_steps` | int | 30 | Sampling steps (10-50) |
| `resolution` | string | "720p" | "480p", "720p", or "1080p" |
| `num_frames` | int | 90 | Number of frames (81-100) |
| `fps` | int | 24 | Frames per second |
| `motion_strength` | int | 7 | Motion intensity (1-10) |
| `sample_shift` | int | 8 | Timing control (1-16) |
| `seed` | int | -1 | Random seed (-1 for random) |

## Response Format

```json
{
  "status": "success",
  "message": "Wan 2.2 text_to_video generation completed",
  "video_base64": "base64_encoded_video_data",
  "filename": "wan2_t2v_output_00001.mp4",
  "generation_type": "text_to_video",
  "prompt": "Your prompt here",
  "settings": {
    "resolution": "720p",
    "frames": 90,
    "guidance_scale": 4.0,
    "steps": 30,
    "motion_strength": 7
  }
}
```

## Deployment

### Prerequisites

1. Docker installed
2. RunPod account with API key
3. Docker registry access (Docker Hub, etc.)

### Steps

1. **Set your RunPod API key**:
   ```bash
   export RUNPOD_API_KEY=your_runpod_api_key_here
   ```

2. **Update registry in deploy.sh**:
   Edit `REGISTRY_IMAGE` in `deploy.sh` to point to your Docker registry.

3. **Deploy**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Update your application**:
   Set the new RunPod endpoint URL in your environment variables.

## Hardware Requirements

- **Minimum**: 80GB VRAM (A100 80GB recommended)
- **Storage**: 100GB for models and outputs
- **Memory**: 32GB+ system RAM

## Cost Estimation

- **480p**: ~$0.00019/second
- **720p**: ~$0.00031/second
- **1080p**: ~$0.00076/second

## Tips for Best Results

1. **CFG Scale**: Use 3-5 for Wan 2.2 (lower than typical models)
2. **Prompt Quality**: Be descriptive but not overly complex
3. **Motion Strength**: Adjust based on desired animation intensity
4. **Resolution**: Start with 720p for best quality/speed balance
5. **Frames**: 90 frames gives good 3-4 second videos at 24fps

## Troubleshooting

### Common Issues

1. **Out of Memory**: Reduce resolution or frames
2. **Slow Generation**: Use fewer inference steps (20-30)
3. **Poor Quality**: Increase CFG scale or steps
4. **No Motion**: Increase motion_strength parameter

### Debug Mode

Set environment variable `DEBUG=1` to enable verbose logging.

## Support

For issues related to:
- **Models**: Check the respective HuggingFace repositories
- **ComfyUI**: Visit the ComfyUI documentation
- **RunPod**: Check RunPod support documentation

## License

This deployment uses open-source models and tools. Check individual model licenses for usage terms.