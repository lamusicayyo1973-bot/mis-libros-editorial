# -*- coding: utf-8 -*-
import sys
import os
import io
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
out_path1 = r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5\escena_c4_e3.jpg"
out_path2 = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-5\escena_c4_e3.jpg"

print(f"Loading SDXL Pipeline from {ckpt_path} on GPU...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

prompt = "Anime style, dark fantasy manga illustration, small demon disintegrating into glowing embers, crystal fan demon retreating into a dark portal, morning sun rising, masterpiece artwork"

print(f"Generating image for prompt: {prompt}")
image = pipe(prompt=prompt, num_inference_steps=25, guidance_scale=7.5, width=1152, height=648).images[0]

image.save(out_path1)
image.save(out_path2)
print(f"REAL AI Image successfully saved to:\n  {out_path1}\n  {out_path2}")
