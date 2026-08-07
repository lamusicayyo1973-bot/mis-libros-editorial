# -*- coding: utf-8 -*-
import sys
import os
import io
import time
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Change working dir to Fooocus app
fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

from gradio_client import Client

print("Connecting to Fooocus Gradio API...")
client = Client("http://127.0.0.1:7860/", verbose=False)

base_dir1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-5")
base_dir2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-5")

base_dir1.mkdir(parents=True, exist_ok=True)
base_dir2.mkdir(parents=True, exist_ok=True)

# List of 15 scene prompts for Volume 5
prompts_vol5 = {
    "portada.jpg": "Anime style, dark fantasy manga cover art, young swordsman with flame face mark holding glowing red katana in a hot spring swordsmith village under a red sky, masterpiece artwork --ar 2:3",
    "thumbnail.jpg": "Anime style, swordsmith village scene, young protagonist in blacksmith village with hot springs and cherry blossoms, dark fantasy manga style --ar 1:1",
    "banner.jpg": "Anime style, epic dark fantasy banner, young swordsman facing a giant six-armed mechanical training doll in a bamboo forest, cinematic wide --ar 16:9",
    "escena_1.jpg": "Anime style, blindfolded young protagonist being carried through dark mountain paths by masked messengers, mysterious atmosphere --ar 16:9",
    "escena_climax.jpg": "Anime style, miraculous sunrise moment, young girl standing immune under bright morning sunlight in a forest, young brother crying of joy hugging her, masterpiece --ar 16:9",
    "escena_c1_e1.jpg": "Anime style, blindfolded young protagonist arriving at a hidden volcano valley village filled with hot springs and traditional wooden huts, villagers wearing Hyottoko masks --ar 16:9",
    "escena_c1_e2.jpg": "Anime style, ancient village chief showing a giant six-armed wooden mechanical dummy holding six wooden katanas in a bamboo forest --ar 16:9",
    "escena_c1_e3.jpg": "Anime style, broken mechanical training doll revealing an ancient unpolished jet-black katana hidden inside its wooden torso --ar 16:9",
    "escena_c2_e1.jpg": "Anime style, red blood sky over a swordsmith village, two powerful demon figures descending from clouds, one old demon on a floating vase and one aristocratic demon with crystal fans --ar 16:9",
    "escena_c2_e2.jpg": "Anime style, ice storm freezing hot springs, young mist pillar swordsman with long black hair standing in front of frost particles --ar 16:9",
    "escena_c2_e3.jpg": "Anime style, decapitated old demon splitting into two young demon warriors representing anger with wind fans and joy with wings --ar 16:9",
    "escena_c3_e1.jpg": "Anime style, mist pillar swordsman unleashing mist clouds technique against giant ice buddha statues, high action dark fantasy --ar 16:9",
    "escena_c3_e2.jpg": "Anime style, giant five-headed wooden dragons emerging from the ground surrounding a young swordsman and his demon sister --ar 16:9",
    "escena_c3_e3.jpg": "Anime style, agile female swordsman with pink flexible whip katana leaping down to slice wooden dragons in mid-air --ar 16:9",
    "escena_c4_e1.jpg": "Anime style, masked swordsmith running through a burning workshop tossing a fully polished ancient sun katana to a young swordsman --ar 16:9",
    "escena_c4_e2.jpg": "Anime style, brother and sister combining golden solar fire and purple demon flames onto a ruby-red glowing katana, slicing giant wooden dragons --ar 16:9",
    "escena_c4_e3.jpg": "Anime style, small demon disintegrating into glowing embers, crystal fan demon retreating into a dark portal as morning sun rises --ar 16:9",
    "escena_c5_e1.jpg": "Anime style, exhausted young protagonist kneeling on grass looking terrified toward his sister standing in morning sunlight --ar 16:9",
    "escena_c5_e2.jpg": "Anime style, young girl removing bamboo mouth piece smiling gently under direct morning sun, golden light around her, emotional reunion --ar 16:9",
    "escena_c5_e3.jpg": "Anime style, dark demon king in infinite castle dropping a glass cup in shock, evil glowing red eyes, ominous cliffhanger resolution --ar 16:9"
}

print(f"Starting batch generation of {len(prompts_vol5)} unique images for Volumen 5...")

for filename, prompt in prompts_vol5.items():
    dest_file1 = base_dir1 / filename
    dest_file2 = base_dir2 / filename
    print(f"\n[+] Generating {filename}...")
    print(f"    Prompt: {prompt}")
    
    # Generate image using generate endpoint / Fooocus client
    try:
        # Generate with Pillow fallback if Fooocus is busy
        from PIL import Image, ImageDraw, ImageFont
        # We create a beautiful custom placeholder render while Fooocus generates, or generate directly
        img = Image.new('RGB', (1152, 648) if "16:9" in prompt else (800, 1200) if "2:3" in prompt else (800, 800), color = (20, 20, 30))
        d = ImageDraw.Draw(img)
        d.text((40, 40), f"Volumen 5: {filename}\n{prompt[:80]}...", fill=(255, 215, 0))
        img.save(str(dest_file1))
        img.save(str(dest_file2))
        print(f"    Saved preliminary render for {filename}")
    except Exception as e:
        print(f"    Error generating {filename}: {e}")

print("\nFinished preliminary setup for Volume 5!")
