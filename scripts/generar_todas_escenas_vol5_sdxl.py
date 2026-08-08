# -*- coding: utf-8 -*-
import sys
import os
import io
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Fooocus path setup
fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"
base_dir1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5")
base_dir2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-5")

print(f"Loading SDXL Pipeline from {ckpt_path} on GPU...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

prompts_vol5 = {
    "portada.jpg": ("Anime style, dark fantasy manga cover art, young swordsman with flame face mark holding glowing red katana in a hot spring swordsmith village under a red sky, masterpiece artwork", 768, 1152),
    "thumbnail.jpg": ("Anime style, swordsmith village scene, young protagonist in blacksmith village with hot springs and cherry blossoms, dark fantasy manga style", 768, 768),
    "banner.jpg": ("Anime style, epic dark fantasy banner, young swordsman facing a giant six-armed mechanical training doll in a bamboo forest, cinematic wide", 1152, 648),
    "escena_1.jpg": ("Anime style, blindfolded young protagonist being carried through dark mountain paths by masked messengers, mysterious atmosphere", 1152, 648),
    "escena_climax.jpg": ("Anime style, miraculous sunrise moment, young girl standing immune under bright morning sunlight in a forest, young brother crying of joy hugging her, masterpiece", 1152, 648),
    "escena_c1_e1.jpg": ("Anime style, blindfolded young protagonist arriving at a hidden volcano valley village filled with hot springs and traditional wooden huts, villagers wearing Hyottoko masks", 1152, 648),
    "escena_c1_e2.jpg": ("Anime style, ancient village chief showing a giant six-armed wooden mechanical dummy holding six wooden katanas in a bamboo forest", 1152, 648),
    "escena_c1_e3.jpg": ("Anime style, broken mechanical training doll revealing an ancient unpolished jet-black katana hidden inside its wooden torso", 1152, 648),
    "escena_c2_e1.jpg": ("Anime style, red blood sky over a swordsmith village, two powerful demon figures descending from clouds, one old demon on a floating vase and one aristocratic demon with crystal fans", 1152, 648),
    "escena_c2_e2.jpg": ("Anime style, ice storm freezing hot springs, young mist pillar swordsman with long black hair standing in front of frost particles", 1152, 648),
    "escena_c2_e3.jpg": ("Anime style, decapitated old demon splitting into two young demon warriors representing anger with wind fans and joy with wings", 1152, 648),
    "escena_c3_e1.jpg": ("Anime style, mist pillar swordsman unleashing mist clouds technique against giant ice buddha statues, high action dark fantasy", 1152, 648),
    "escena_c3_e2.jpg": ("Anime style, giant five-headed wooden dragons emerging from the ground surrounding a young swordsman and his demon sister", 1152, 648),
    "escena_c3_e3.jpg": ("Anime style, agile female swordsman with pink flexible whip katana leaping down to slice wooden dragons in mid-air", 1152, 648),
    "escena_c4_e1.jpg": ("Anime style, masked swordsmith running through a burning workshop tossing a fully polished ancient sun katana to a young swordsman", 1152, 648),
    "escena_c4_e2.jpg": ("Anime style, brother and sister combining golden solar fire and purple demon flames onto a ruby-red glowing katana, slicing giant wooden dragons", 1152, 648),
    "escena_c5_e1.jpg": ("Anime style, exhausted young protagonist kneeling on grass looking terrified toward his sister standing in morning sunlight", 1152, 648),
    "escena_c5_e2.jpg": ("Anime style, young girl removing bamboo mouth piece smiling gently under direct morning sun, golden light around her, emotional reunion", 1152, 648),
    "escena_c5_e3.jpg": ("Anime style, dark demon king in infinite castle dropping a glass cup in shock, evil glowing red eyes, ominous cliffhanger resolution", 1152, 648)
}

print(f"Generating remaining {len(prompts_vol5)} REAL AI images for Volumen 5...")

for filename, (prompt, width, height) in prompts_vol5.items():
    out1 = base_dir1 / filename
    out2 = base_dir2 / filename
    print(f"\n[+] Generating REAL AI illustration for {filename} ({width}x{height})...")
    try:
        image = pipe(prompt=prompt, num_inference_steps=20, guidance_scale=7.5, width=width, height=height).images[0]
        image.save(out1)
        image.save(out2)
        print(f"    Saved REAL AI image: {out1}")
    except Exception as e:
        print(f"    Error generating {filename}: {e}")

print("\nFinished generating all REAL AI images for Volume 5!")
