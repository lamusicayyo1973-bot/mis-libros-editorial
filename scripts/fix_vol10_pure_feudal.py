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

NEGATIVE = (
    "modern, modern city, skyscrapers, cars, modern clothes, suits, t-shirt, jeans, "
    "child, kid, toddler, baby, young child, primary school student, kindergarten, "
    "mask, surgical mask, face mask, robot, mecha, 3d render, photorealistic photo, "
    "plastic doll, lowres, blurry, ugly, watermark, text, logo, extra arms, extra limbs, bad anatomy"
)

print("Loading SDXL Pipeline...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

# 100% Feudal Japan Epilogue Prompts - No modern elements whatsoever
prompts_to_fix = {
    "escena_c5_e1.jpg": (
        "anime dark fantasy illustration, peaceful morning sunrise over ancient feudal Japanese mountain village, "
        "traditional wooden houses, mist rising over green rice terraces and cherry blossoms, serene atmosphere",
        1152, 648
    ),
    "escena_c5_e2.jpg": (
        "anime dark fantasy illustration, victorious warriors of the solar brotherhood resting peacefully on wooden porch of traditional Japanese house, "
        "drinking tea together in morning sun, peaceful feudal setting",
        1152, 648
    ),
    "escena_c5_e3.jpg": (
        "anime dark fantasy illustration, handsome 19 year old samurai Ren in dark traditional kimono and his 18 year old sister Miyuki in pink kimono "
        "walking together on a stone path under blooming cherry blossom trees in their mountain village, smiling peacefully, masterpiece",
        1152, 648
    ),
    "escena_climax.jpg": (
        "anime dark fantasy illustration, handsome 19 year old samurai Ren hanging up his solar katana on a wooden display stand in his family blacksmith home, "
        "golden sunlight streaming through paper shoji doors, peaceful grand finale, masterpiece",
        1152, 648
    )
}

print(f"\nRegenerando escenas del Capítulo 5 del Volumen 10 (100% Época Feudal Japonesa)...")

for filename, (prompt, width, height) in prompts_to_fix.items():
    out1 = vol10_dir1 / filename
    out2 = vol10_dir2 / filename
    print(f"[+] Generando {filename} en época feudal ({width}x{height})...")
    image = pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE,
        num_inference_steps=28,
        guidance_scale=8.5,
        width=width,
        height=height
    ).images[0]
    image.save(out1)
    image.save(out2)
    print(f"    Guardada: {out1}")

print("\n¡Capítulo 5 del Volumen 10 corregido 100% a la época feudal japonesa!")
