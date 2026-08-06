import os
os.environ["XFORMERS_PACKAGE_IS_DISABLED"] = "1"
os.environ["XFORMERS_DISABLED"] = "1"

import sys
import torch
from diffusers import StableDiffusionXLPipeline

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"

print(f"Loading local SDXL model on RTX 3060: {ckpt_path}")

pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

def generate_local_image(prompt, output_path, aspect_ratio="16:9"):
    if aspect_ratio == "3:4":
        w, h = 768, 1024
    elif aspect_ratio == "1:1":
        w, h = 1024, 1024
    else:
        w, h = 1024, 576
        
    print(f"Generating image locally on RTX 3060 ({w}x{h})...")
    image = pipe(
        prompt=prompt,
        negative_prompt="low quality, blurry, bad anatomy, worst quality, text watermark",
        num_inference_steps=25,
        guidance_scale=7.5,
        width=w,
        height=h
    ).images[0]
    
    image.save(output_path)
    print(f"Image saved successfully to {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) > 2:
        prompt_in = sys.argv[1]
        out_in = sys.argv[2]
        ar_in = sys.argv[3] if len(sys.argv) > 3 else "16:9"
        generate_local_image(prompt_in, out_in, ar_in)
