"""
Unified RunPod Handler for Wan 2.2 Video Generation
Supports both Text-to-Video and Image-to-Video using the latest Wan 2.2 models
"""
import os
import sys
import json
import uuid
import requests
import base64
import subprocess
import time
import asyncio
from pathlib import Path
import runpod

# ComfyUI integration
sys.path.append('/workspace/ComfyUI')

class Wan2VideoGenerator:
    def __init__(self):
        self.comfyui_url = "http://localhost:8188"
        self.model_paths = {
            'text_to_video': {
                'high_noise': '/workspace/ComfyUI/models/diffusion_models/wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors',
                'low_noise': '/workspace/ComfyUI/models/diffusion_models/wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors'
            },
            'image_to_video': {
                'high_noise': '/workspace/ComfyUI/models/diffusion_models/wan2.2_i2v_high_noise_14B_fp16.safetensors',
                'low_noise': '/workspace/ComfyUI/models/diffusion_models/wan2.2_i2v_low_noise_14B_fp16.safetensors'
            },
            'vae': '/workspace/ComfyUI/models/vae/wan_2.1_vae.safetensors',
            'text_encoder': '/workspace/ComfyUI/models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors'
        }
        
    def download_models(self):
        """Download required models if not present"""
        model_urls = {
            # Text-to-Video models from NSFW-API repository
            'wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors': 'https://huggingface.co/NSFW-API/NSFW_Wan_14b/resolve/main/wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors',
            'wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors': 'https://huggingface.co/NSFW-API/NSFW_Wan_14b/resolve/main/wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors',
            
            # Image-to-Video models from Wan-AI repository
            'wan2.2_i2v_high_noise_14B_fp16.safetensors': 'https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B/resolve/main/wan2.2_i2v_high_noise_14B_fp16.safetensors',
            'wan2.2_i2v_low_noise_14B_fp16.safetensors': 'https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B/resolve/main/wan2.2_i2v_low_noise_14B_fp16.safetensors',
            
            # Shared components
            'wan_2.1_vae.safetensors': 'https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/vae/wan_2.1_vae.safetensors',
            'umt5_xxl_fp8_e4m3fn_scaled.safetensors': 'https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors'
        }
        
        download_paths = {
            'wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors': '/workspace/ComfyUI/models/diffusion_models/',
            'wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors': '/workspace/ComfyUI/models/diffusion_models/',
            'wan2.2_i2v_high_noise_14B_fp16.safetensors': '/workspace/ComfyUI/models/diffusion_models/',
            'wan2.2_i2v_low_noise_14B_fp16.safetensors': '/workspace/ComfyUI/models/diffusion_models/',
            'wan_2.1_vae.safetensors': '/workspace/ComfyUI/models/vae/',
            'umt5_xxl_fp8_e4m3fn_scaled.safetensors': '/workspace/ComfyUI/models/text_encoders/'
        }
        
        for filename, url in model_urls.items():
            local_path = os.path.join(download_paths[filename], filename)
            
            if not os.path.exists(local_path):
                print(f"📥 Downloading {filename}...")
                self._download_file(url, local_path)
            else:
                print(f"✅ {filename} already exists")
    
    def _download_file(self, url, filepath):
        """Download file with progress tracking"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"📊 Progress: {progress:.1f}% ({downloaded}/{total_size} bytes)")
            
            print(f"✅ Downloaded {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def create_text_to_video_workflow(self, params):
        """Create ComfyUI workflow for text-to-video generation"""
        return {
            "1": {
                "class_type": "Wan2CheckpointLoader",
                "inputs": {
                    "ckpt_name_high_noise": "wan2.2_t2v_high_noise_14B_fp8_scaled.safetensors",
                    "ckpt_name_low_noise": "wan2.2_t2v_low_noise_14B_fp8_scaled.safetensors",
                    "vae_name": "wan_2.1_vae.safetensors"
                }
            },
            "2": {
                "class_type": "Wan2TextEncode",
                "inputs": {
                    "text": params.get('prompt', ''),
                    "text_encoder_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
                }
            },
            "3": {
                "class_type": "Wan2TextEncode", 
                "inputs": {
                    "text": params.get('negative_prompt', 'blurry, bad quality, camera shake, distortion, poor composition, low resolution, artifacts'),
                    "text_encoder_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
                }
            },
            "4": {
                "class_type": "Wan2EmptyLatentVideo",
                "inputs": {
                    "width": self._get_resolution_dimensions(params.get('resolution', '720p'))[0],
                    "height": self._get_resolution_dimensions(params.get('resolution', '720p'))[1],
                    "frames": params.get('num_frames', 90),
                    "batch_size": 1
                }
            },
            "5": {
                "class_type": "Wan2Sampler",
                "inputs": {
                    "model": ["1", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "latent_image": ["4", 0],
                    "seed": params.get('seed', -1),
                    "steps": params.get('num_inference_steps', 30),
                    "cfg": params.get('guidance_scale', 4.0),
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "sample_shift": params.get('sample_shift', 8),
                    "motion_strength": params.get('motion_strength', 7)
                }
            },
            "6": {
                "class_type": "Wan2VAEDecode",
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["1", 2]
                }
            },
            "7": {
                "class_type": "Wan2SaveVideo",
                "inputs": {
                    "images": ["6", 0],
                    "filename_prefix": "wan2_t2v_output",
                    "fps": params.get('fps', 24),
                    "save_image": True,
                    "pingpong": False,
                    "save_output": True
                }
            }
        }
    
    def create_image_to_video_workflow(self, params):
        """Create ComfyUI workflow for image-to-video generation"""
        return {
            "1": {
                "class_type": "Wan2CheckpointLoader",
                "inputs": {
                    "ckpt_name_high_noise": "wan2.2_i2v_high_noise_14B_fp16.safetensors",
                    "ckpt_name_low_noise": "wan2.2_i2v_low_noise_14B_fp16.safetensors",
                    "vae_name": "wan_2.1_vae.safetensors"
                }
            },
            "2": {
                "class_type": "LoadImageFromURL",
                "inputs": {
                    "url": params.get('image_url', '')
                }
            },
            "3": {
                "class_type": "Wan2TextEncode",
                "inputs": {
                    "text": params.get('prompt', 'animate this image with smooth motion'),
                    "text_encoder_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
                }
            },
            "4": {
                "class_type": "Wan2TextEncode",
                "inputs": {
                    "text": params.get('negative_prompt', 'blurry, bad quality, camera shake, distortion, poor composition, low resolution, artifacts'),
                    "text_encoder_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
                }
            },
            "5": {
                "class_type": "Wan2ImageToVideo",
                "inputs": {
                    "image": ["2", 0],
                    "width": self._get_resolution_dimensions(params.get('resolution', '720p'))[0],
                    "height": self._get_resolution_dimensions(params.get('resolution', '720p'))[1],
                    "frames": params.get('num_frames', 90),
                    "batch_size": 1
                }
            },
            "6": {
                "class_type": "Wan2Sampler",
                "inputs": {
                    "model": ["1", 0],
                    "positive": ["3", 0],
                    "negative": ["4", 0],
                    "latent_image": ["5", 0],
                    "seed": params.get('seed', -1),
                    "steps": params.get('num_inference_steps', 30),
                    "cfg": params.get('guidance_scale', 4.0),
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "sample_shift": params.get('sample_shift', 8),
                    "motion_strength": params.get('motion_strength', 7)
                }
            },
            "7": {
                "class_type": "Wan2VAEDecode",
                "inputs": {
                    "samples": ["6", 0],
                    "vae": ["1", 2]
                }
            },
            "8": {
                "class_type": "Wan2SaveVideo",
                "inputs": {
                    "images": ["7", 0],
                    "filename_prefix": "wan2_i2v_output",
                    "fps": params.get('fps', 24),
                    "save_image": True,
                    "pingpong": False,
                    "save_output": True
                }
            }
        }
    
    def _get_resolution_dimensions(self, resolution):
        """Convert resolution string to width/height"""
        resolutions = {
            '480p': (854, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080)
        }
        return resolutions.get(resolution, (1280, 720))
    
    def start_comfyui_server(self):
        """Start ComfyUI server"""
        try:
            print("🚀 Starting ComfyUI server...")
            process = subprocess.Popen([
                'python', '/workspace/ComfyUI/main.py', 
                '--listen', '0.0.0.0',
                '--port', '8188',
                '--force-fp16'
            ], cwd='/workspace/ComfyUI')
            
            # Wait for server to be ready
            for i in range(30):
                try:
                    response = requests.get(f"{self.comfyui_url}/system_stats")
                    if response.status_code == 200:
                        print("✅ ComfyUI server is ready!")
                        return process
                except:
                    time.sleep(2)
            
            raise Exception("ComfyUI server failed to start")
            
        except Exception as e:
            print(f"❌ Failed to start ComfyUI server: {e}")
            raise
    
    def execute_workflow(self, workflow):
        """Execute ComfyUI workflow and return result"""
        try:
            client_id = str(uuid.uuid4())
            
            # Queue workflow
            queue_response = requests.post(
                f"{self.comfyui_url}/prompt",
                json={"prompt": workflow, "client_id": client_id}
            )
            queue_response.raise_for_status()
            
            prompt_id = queue_response.json()["prompt_id"]
            print(f"📤 Workflow queued with ID: {prompt_id}")
            
            # Poll for completion
            start_time = time.time()
            timeout = 600  # 10 minutes
            
            while time.time() - start_time < timeout:
                try:
                    history_response = requests.get(f"{self.comfyui_url}/history/{prompt_id}")
                    
                    if history_response.status_code == 200:
                        history_data = history_response.json()
                        
                        if prompt_id in history_data:
                            outputs = history_data[prompt_id].get('outputs', {})
                            
                            # Find video output
                            for node_id, output_data in outputs.items():
                                if 'gifs' in output_data and output_data['gifs']:
                                    video_info = output_data['gifs'][0]
                                    video_path = f"/workspace/ComfyUI/output/{video_info['filename']}"
                                    
                                    if os.path.exists(video_path):
                                        # Convert to base64
                                        with open(video_path, 'rb') as f:
                                            video_base64 = base64.b64encode(f.read()).decode('utf-8')
                                        
                                        return {
                                            'success': True,
                                            'video_base64': video_base64,
                                            'filename': video_info['filename']
                                        }
                    
                except requests.RequestException:
                    pass
                
                time.sleep(5)
            
            return {'success': False, 'error': 'Generation timeout'}
            
        except Exception as e:
            print(f"❌ Workflow execution error: {e}")
            return {'success': False, 'error': str(e)}

# Global generator instance
generator = Wan2VideoGenerator()
comfyui_process = None

def handler(job):
    """Main RunPod handler for Wan 2.2 video generation"""
    global comfyui_process
    
    try:
        job_input = job.get('input', {})
        print(f"🎬 Processing Wan 2.2 generation request...")
        
        # Download models if needed
        generator.download_models()
        
        # Start ComfyUI server if not running
        if comfyui_process is None:
            comfyui_process = generator.start_comfyui_server()
        
        # Determine generation type
        is_image_to_video = 'image_url' in job_input and job_input['image_url']
        generation_type = 'image_to_video' if is_image_to_video else 'text_to_video'
        
        print(f"🎥 Generation mode: {generation_type}")
        
        # Create appropriate workflow
        if is_image_to_video:
            workflow = generator.create_image_to_video_workflow(job_input)
        else:
            workflow = generator.create_text_to_video_workflow(job_input)
        
        # Execute workflow
        result = generator.execute_workflow(workflow)
        
        if result['success']:
            return {
                "status": "success",
                "message": f"Wan 2.2 {generation_type} generation completed",
                "video_base64": result['video_base64'],
                "filename": result['filename'],
                "generation_type": generation_type,
                "prompt": job_input.get('prompt', ''),
                "settings": {
                    "resolution": job_input.get('resolution', '720p'),
                    "frames": job_input.get('num_frames', 90),
                    "guidance_scale": job_input.get('guidance_scale', 4.0),
                    "steps": job_input.get('num_inference_steps', 30),
                    "motion_strength": job_input.get('motion_strength', 7)
                }
            }
        else:
            return {"error": result['error']}
    
    except Exception as e:
        print(f"❌ Handler error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("🚀 Starting Wan 2.2 RunPod Serverless Handler")
    print("✅ Supports both Text-to-Video and Image-to-Video generation")
    print("🎯 Models: NSFW-API/NSFW_Wan_14b + Wan-AI/Wan2.2-I2V-A14B")
    
    runpod.serverless.start({"handler": handler})