import urllib.request
import json
import time

prompt_text = "An ultra-premium 3D manga light novel cover mockup. Title 'ONI NO KETSURYU Vol 2', Author 'NICOLAS NOGUERA'. Epic dark fantasy anime hero with jet-black katana featuring a thin glowing red line."

workflow = {
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "cfg": 8,
      "denoise": 1,
      "latent_image": ["5", 0],
      "model": ["4", 0],
      "negative": ["7", 0],
      "positive": ["6", 0],
      "sampler_name": "euler",
      "scheduler": "normal",
      "seed": 42,
      "steps": 20
    }
  },
  "4": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "juggernautXL_v8Rundiffusion.safetensors"
    }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "inputs": {
      "batch_size": 1,
      "height": 1024,
      "width": 768
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "clip": ["4", 1],
      "text": prompt_text
    }
  },
  "7": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "clip": ["4", 1],
      "text": "low quality, blurry, deformed"
    }
  },
  "8": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": ["3", 0],
      "vae": ["4", 2]
    }
  },
  "9": {
    "class_type": "SaveImage",
    "inputs": {
      "filename_prefix": "oni_vol2_portada_local",
      "images": ["8", 0]
    }
  }
}

p = {"prompt": workflow}
data = json.dumps(p).encode('utf-8')
req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data, headers={'Content-Type': 'application/json'})

try:
    response = urllib.request.urlopen(req)
    res = json.loads(response.read())
    print("Prompt submitted to ComfyUI API successfully! Prompt ID:", res.get("prompt_id"))
except Exception as e:
    print("Error submitting prompt to ComfyUI:", e)
