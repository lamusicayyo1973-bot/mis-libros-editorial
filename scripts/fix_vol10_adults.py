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
    "child, kid, toddler, baby, young child, primary school student, kindergarten, "
    "mask, surgical mask, face mask, modern clothes in feudal scenes, robot, mecha, "
    "3d render, photorealistic photo, plastic doll, lowres, blurry, ugly, watermark, text, logo, "
    "extra arms, extra limbs, extra hands, distorted eyes, bad anatomy"
)

print("Loading SDXL Pipeline...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

# Prompts for Volume 10 with young adult characters (18-20 years old), handsome anime swordsman & maiden
prompts_to_fix = {
    "portada.jpg": (
        "anime dark fantasy manga cover art, handsome 18 year old male swordsman with sun mark and beautiful 17 year old young adult sister "
        "standing side by side under golden morning sunlight on a mountain peak looking at sunrise, falling cherry blossom petals, masterpiece",
        768, 1152
    ),
    "thumbnail.jpg": (
        "anime dark fantasy square thumbnail, beautiful 17 year old maiden holding hand of handsome 18 year old young adult swordsman under golden sunlight, "
        "glowing warm light particles, clean portrait, masterpiece manga style",
        768, 768
    ),
    "escena_1.jpg": (
        "anime dark fantasy illustration, handsome 18 year old young adult swordsman resting on stone wall at dawn after final victory, "
        "golden sunlight breaking through morning mist over ancient japanese town, peaceful emotional scene",
        1152, 648
    ),
    "escena_c1_e1.jpg": (
        "anime dark fantasy illustration, beautiful 17 year old maiden kneeling beside her handsome 18 year old young adult brother resting on grass, "
        "holding his hands as warm golden healing light flows between them",
        1152, 648
    ),
    "escena_c2_e3.jpg": (
        "anime dark fantasy illustration, handsome 18 year old young adult swordsman and his 17 year old sister walking back up mountain path to their old family home, "
        "wooden swordsmith cabin in the distance, sunset light",
        1152, 648
    ),
    "escena_c5_e2.jpg": (
        "anime fantasy illustration, attractive 19 year old college students laughing on sidewalk in modern Tokyo, "
        "reincarnations of the ancient warriors enjoying peaceful modern life under cherry blossoms",
        1152, 648
    ),
    "escena_c5_e3.jpg": (
        "anime fantasy illustration, handsome 19 year old young adult male and attractive 18 year old young adult female walking under pink cherry blossom trees in modern Tokyo, "
        "smiling peacefully at the camera, heartwarming conclusion, masterpiece",
        1152, 648
    ),
    "escena_climax.jpg": (
        "anime fantasy illustration, handsome 19 year old young adult male protagonist standing under blooming cherry trees in modern Tokyo, "
        "holding hand of attractive young adult maiden, golden sunset light, masterpiece grand finale",
        1152, 648
    )
}

print(f"\nRegenerando {len(prompts_to_fix)} imagenes del Volumen 10 con personajes adultos (18-20 años)...")

for filename, (prompt, width, height) in prompts_to_fix.items():
    out1 = vol10_dir1 / filename
    out2 = vol10_dir2 / filename
    print(f"[+] Generando {filename} con personajes adultos ({width}x{height})...")
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

print("\n¡Imágenes del Volumen 10 regeneradas con personajes jóvenes adultos!")
