# -*- coding: utf-8 -*-
import sys
import os
import io
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
base_dir1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5")
base_dir2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-5")

NEGATIVE = (
    "mask, surgical mask, face mask, covid mask, medical mask, blue mask, "
    "robot, mecha, metallic robot, cyborg, futuristic, modern clothes, t-shirt, jeans, "
    "3d render, photorealistic photo, toy figure, lowres, blurry, ugly, watermark, text, logo"
)

print("Loading SDXL Pipeline...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

prompts_to_fix = {
    "banner.jpg": (
        "anime dark fantasy wide banner illustration, young japanese swordsman with katana "
        "training against a giant ancient wooden six-armed samurai puppet in a misty bamboo forest, "
        "torches, fallen leaves, dramatic cinematic lighting, no robot, no metal, "
        "feudal japan setting, masterpiece high quality manga art style",
        1152, 648
    ),
    "escena_1.jpg": (
        "anime dark fantasy illustration, blindfolded young male protagonist being carried "
        "on the back of a ninja messenger wearing a black cloth shinobi face cowl, "
        "travelling through dark rocky mountain paths under a starry night sky, "
        "mysterious atmosphere, feudal japan ninja, no surgical mask, no medical mask, "
        "cinematic lighting, masterpiece manga art style",
        1152, 648
    ),
    "thumbnail.jpg": (
        "anime dark fantasy square thumbnail, young swordsman with a crimson flame mark on his forehead "
        "holding a glowing red katana, hot spring village under cherry blossoms background, "
        "vibrant colors, clean portrait, masterpiece manga cover art style",
        768, 768
    )
}

print(f"\nRegenerando {len(prompts_to_fix)} imagenes (banner, escena_1, thumbnail)...")

for filename, (prompt, width, height) in prompts_to_fix.items():
    out1 = base_dir1 / filename
    out2 = base_dir2 / filename
    print(f"[+] Generando {filename} ({width}x{height})...")
    image = pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE,
        num_inference_steps=28,
        guidance_scale=8.0,
        width=width,
        height=height
    ).images[0]
    image.save(out1)
    image.save(out2)
    print(f"    Guardada: {out1}")

print("\n¡Banner, escena_1 y thumbnail regenerados con éxito!")
