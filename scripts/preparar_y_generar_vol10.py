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

vol10_dir1.mkdir(parents=True, exist_ok=True)
vol10_dir2.mkdir(parents=True, exist_ok=True)

# 1. Delete old images in Volume 10
image_names = [
    "portada.jpg", "thumbnail.jpg", "banner.jpg", "escena_1.jpg", "escena_climax.jpg",
    "escena_c1_e1.jpg", "escena_c1_e2.jpg", "escena_c1_e3.jpg",
    "escena_c2_e1.jpg", "escena_c2_e2.jpg", "escena_c2_e3.jpg",
    "escena_c3_e1.jpg", "escena_c3_e2.jpg", "escena_c3_e3.jpg",
    "escena_c4_e1.jpg", "escena_c4_e2.jpg", "escena_c4_e3.jpg",
    "escena_c5_e1.jpg", "escena_c5_e2.jpg", "escena_c5_e3.jpg"
]

print("Clearing old images in Volume 10...")
for name in image_names:
    for folder in [vol10_dir1, vol10_dir2]:
        p = folder / name
        if p.exists():
            p.unlink()

print("Old images in Volume 10 deleted!")

# 2. Setup SDXL GPU pipeline
fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"

NEGATIVE = (
    "mask, surgical mask, face mask, modern clothes in feudal scenes, robot, mecha, "
    "3d render, photorealistic photo, plastic doll, lowres, blurry, ugly, watermark, text, logo, "
    "extra arms, extra limbs, extra hands, distorted eyes, bad anatomy"
)

print(f"Loading SDXL Pipeline from {ckpt_path} on GPU...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

# 3. Dedicated custom prompts for Volume 10: El Amanecer del Acero Santo (Grand Finale)
prompts_vol10 = {
    "portada.jpg": (
        "anime dark fantasy manga cover art, young brother and sister standing side by side under golden morning sunlight on a mountain peak, "
        "falling cherry blossom petals, serene peaceful smile, masterpiece grand finale art",
        768, 1152
    ),
    "thumbnail.jpg": (
        "anime dark fantasy square thumbnail, young girl holding her brother's hand under golden sunlight, "
        "glowing warm light particles, emotional peaceful portrait, masterpiece manga style",
        768, 768
    ),
    "banner.jpg": (
        "anime dark fantasy wide banner, peaceful Japanese mountain village at sunrise, "
        "green rice fields, cherry blossoms blooming, mist in valley, masterpiece high quality manga art style",
        1152, 648
    ),
    "escena_1.jpg": (
        "anime dark fantasy illustration, quiet morning after the final battle, golden sun rays piercing through clouds, "
        "ruined city streets bathed in warm peaceful light, emotional dawn scene",
        1152, 648
    ),
    "escena_climax.jpg": (
        "anime fantasy illustration, modern Tokyo city street under full bloom cherry blossom trees, "
        "reincarnations of the brother and sister walking together in modern school uniforms smiling at each other, peaceful grand finale, masterpiece",
        1152, 648
    ),
    "escena_c1_e1.jpg": (
        "anime dark fantasy illustration, young sister kneeling beside her injured brother resting on grass, "
        "holding his hands as warm golden healing light flows between them",
        1152, 648
    ),
    "escena_c1_e2.jpg": (
        "anime dark fantasy illustration, surviving warriors laying their broken katanas down on stone altar, "
        "tears of relief, final ceremony of peace, feudal japan setting",
        1152, 648
    ),
    "escena_c1_e3.jpg": (
        "anime dark fantasy illustration, medical tent at dawn, doctors and kakushi tenders treating wounded heroes, "
        "peaceful atmosphere, morning sunlight",
        1152, 648
    ),
    "escena_c2_e1.jpg": (
        "anime dark fantasy illustration, emotional reunion of surviving comrades embracing under morning sky, "
        "weeping tears of joy, dramatic heartfelt moment",
        1152, 648
    ),
    "escena_c2_e2.jpg": (
        "anime dark fantasy illustration, disbanding ceremony of the solar brotherhood guild, "
        "warriors bowing to each other before parting ways under cherry blossoms",
        1152, 648
    ),
    "escena_c2_e3.jpg": (
        "anime dark fantasy illustration, young brother and sister walking back up mountain path to their old family home, "
        "wooden swordsmith cabin in the distance, sunset light",
        1152, 648
    ),
    "escena_c3_e1.jpg": (
        "anime dark fantasy illustration, young protagonist putting away his solar katana into a wooden display case inside his home, "
        "peaceful indoor setting",
        1152, 648
    ),
    "escena_c3_e2.jpg": (
        "anime dark fantasy illustration, brother and sister tending a garden of wisteria and roses together, "
        "sunny afternoon, warm tranquil lifestyle",
        1152, 648
    ),
    "escena_c3_e3.jpg": (
        "anime dark fantasy illustration, old wooden forge transformed into a peaceful blacksmith shop making agricultural tools, "
        "warm hearth fire, peaceful village life",
        1152, 648
    ),
    "escena_c4_e1.jpg": (
        "anime dark fantasy illustration, elderly master looking at old framed painting of the ancient warriors, "
        "passing the story to young children sitting around tatami room",
        1152, 648
    ),
    "escena_c4_e2.jpg": (
        "anime dark fantasy illustration, quiet starry night over mountain shrine, "
        "two glowing paper lanterns floating into the night sky carrying prayers of gratitude",
        1152, 648
    ),
    "escena_c4_e3.jpg": (
        "anime dark fantasy illustration, sun rising over misty Japanese mountains, "
        "symbolic golden solar crest shining in the sky above ancient forest",
        1152, 648
    ),
    "escena_c5_e1.jpg": (
        "anime fantasy illustration, modern Tokyo skyline at sunrise, "
        "tall skyscrapers illuminated by warm golden morning light, transition to modern era",
        1152, 648
    ),
    "escena_c5_e2.jpg": (
        "anime fantasy illustration, modern high school students laughing on sidewalk in Tokyo, "
        "reincarnations of the ancient Hashira warriors enjoying peaceful modern life",
        1152, 648
    ),
    "escena_c5_e3.jpg": (
        "anime fantasy illustration, young boy with sun earrings and his sister walking under pink cherry blossom trees in modern Tokyo, "
        "smiling peacefully at the camera, heartwarming conclusion",
        1152, 648
    )
}

print(f"\nGenerating all {len(prompts_vol10)} REAL AI images for Volume 10...")

for filename, (prompt, width, height) in prompts_vol10.items():
    out1 = vol10_dir1 / filename
    out2 = vol10_dir2 / filename
    print(f"[+] Generating Volume 10 illustration for {filename} ({width}x{height})...")
    try:
        image = pipe(
            prompt=prompt,
            negative_prompt=NEGATIVE,
            num_inference_steps=25,
            guidance_scale=8.0,
            width=width,
            height=height
        ).images[0]
        image.save(out1)
        image.save(out2)
        print(f"    Saved: {out1}")
    except Exception as e:
        print(f"    Error generating {filename}: {e}")

print("\nFinished generating all REAL AI images for Volume 10!")
