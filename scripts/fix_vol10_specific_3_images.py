# -*- coding: utf-8 -*-
import sys
import os
import io
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

vol10_dir1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-10")
vol10_dir2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-10")

fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"

print("Loading SDXL Pipeline...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

# Specific fixes requested by user:
# 1. escena_c3_e2: NO children! Adult anime characters in wisteria garden
# 2. escena_c5_e3: NO photorealistic real people! Pure anime manga illustration style
# 3. thumbnail: NO blonde hair! Miyuki must have dark hair
prompts_to_fix = {
    "thumbnail.jpg": (
        "anime dark fantasy square thumbnail, beautiful 18 year old Japanese maiden Miyuki with long dark hair and brown eyes "
        "holding hand of handsome 19 year old samurai Ren with dark hair under golden sunlight, glowing warm light particles, clean anime manga portrait, masterpiece",
        "blonde hair, yellow hair, fair hair, light hair, photorealistic, photo, child, kid, modern, 3d render, lowres, blurry",
        768, 768
    ),
    "escena_c3_e2.jpg": (
        "anime dark fantasy illustration, handsome 19 year old samurai Ren with dark hair and 18 year old maiden Miyuki with long dark hair, "
        "standing together in a lush garden of purple wisteria and pink roses at sunset, serene peaceful setting, 2d anime manga art style, masterpiece",
        "child, kid, toddler, baby, photorealistic, photo, real person, blonde, yellow hair, modern, 3d render, lowres, blurry",
        1152, 648
    ),
    "escena_c5_e3.jpg": (
        "anime dark fantasy illustration, handsome 19 year old samurai Ren in dark traditional kimono and 18 year old maiden Miyuki in pink traditional kimono, "
        "both with long dark hair, walking together on a stone path under blooming cherry blossom trees in mountain village, 2d anime drawing, masterpiece studio ghibli ufotable style",
        "photorealistic photo, real person, photograph, realistic photography, 3d render, modern clothes, child, kid, blonde, yellow hair, lowres, blurry",
        1152, 648
    )
}

print(f"\nRegenerando {len(prompts_to_fix)} imagenes especificas del Volumen 10...")

for filename, (prompt, neg, width, height) in prompts_to_fix.items():
    out1 = vol10_dir1 / filename
    out2 = vol10_dir2 / filename
    print(f"[+] Generando {filename} ({width}x{height})...")
    image = pipe(
        prompt=prompt,
        negative_prompt=neg,
        num_inference_steps=30,
        guidance_scale=8.5,
        width=width,
        height=height
    ).images[0]
    image.save(out1)
    image.save(out2)
    print(f"    Guardada: {out1}")

print("\n¡Las 3 imágenes especificas del Volumen 10 fueron corregidas con éxito!")
