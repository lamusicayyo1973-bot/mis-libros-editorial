# -*- coding: utf-8 -*-
import sys
import os
import io
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

vol6_dir1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-6")
vol6_dir2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-6")

vol6_dir1.mkdir(parents=True, exist_ok=True)
vol6_dir2.mkdir(parents=True, exist_ok=True)

# 1. Delete all existing old/placeholder images in Vol 6
image_names = [
    "portada.jpg", "thumbnail.jpg", "banner.jpg", "escena_1.jpg", "escena_climax.jpg",
    "escena_c1_e1.jpg", "escena_c1_e2.jpg", "escena_c1_e3.jpg",
    "escena_c2_e1.jpg", "escena_c2_e2.jpg", "escena_c2_e3.jpg",
    "escena_c3_e1.jpg", "escena_c3_e2.jpg", "escena_c3_e3.jpg",
    "escena_c4_e1.jpg", "escena_c4_e2.jpg", "escena_c4_e3.jpg",
    "escena_c5_e1.jpg", "escena_c5_e2.jpg", "escena_c5_e3.jpg"
]

print("Clearing old images in Volume 6...")
for name in image_names:
    for folder in [vol6_dir1, vol6_dir2]:
        p = folder / name
        if p.exists():
            p.unlink()

print("Old images deleted!")

# 2. Setup SDXL GPU pipeline
fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"

NEGATIVE = (
    "mask, surgical mask, face mask, modern clothes, t-shirt, jeans, robot, mecha, "
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

# 3. Dedicated custom prompts for Volume 6: Las Catacumbas del Olvido
prompts_vol6 = {
    "portada.jpg": (
        "anime dark fantasy manga cover art, tall imposing six-eyed samurai demon in purple kimono holding a flesh katana, "
        "standing in dark underground stone catacombs with glowing purple runes, epic dark atmosphere, masterpiece",
        768, 1152
    ),
    "thumbnail.jpg": (
        "anime dark fantasy square thumbnail, young samurai with glowing sun mark on forehead standing under purple wisteria trees, "
        "vibrant colors, clean portrait, masterpiece manga art style",
        768, 768
    ),
    "banner.jpg": (
        "anime dark fantasy wide banner, grand wisteria sanctuary mansion surrounded by glowing purple trees under a starry night, "
        "swordsmen training in courtyard, masterpiece high quality manga style",
        1152, 648
    ),
    "escena_1.jpg": (
        "anime dark fantasy illustration, young swordsman arriving at a sacred estate overflowing with blooming purple wisteria flowers, "
        "warm lantern light, peaceful traditional Japanese sanctuary",
        1152, 648
    ),
    "escena_climax.jpg": (
        "anime dark fantasy illustration, massive explosion rocking a traditional Japanese mansion at night, "
        "flames and wooden debris flying everywhere, demon lord stepping through smoke, epic climactic moment, masterpiece manga style",
        1152, 648
    ),
    "escena_c1_e1.jpg": (
        "anime dark fantasy illustration, group of elite Sables de Elite pillars in colorful haori coats assembled in a tatami room, "
        "serious warrior meeting under wisteria decorations, feudal japan setting",
        1152, 648
    ),
    "escena_c1_e2.jpg": (
        "anime dark fantasy illustration, young swordsman dodging massive boulders thrown by a muscular blind Pillar warrior in a rocky ravine, "
        "intense training session, dust rising, action pose",
        1152, 648
    ),
    "escena_c1_e3.jpg": (
        "anime dark fantasy illustration, young swordsman meditating under a freezing waterfall, sun mark glowing on his forehead, "
        "determination in his eyes, water splashing, master level endurance training",
        1152, 648
    ),
    "escena_c2_e1.jpg": (
        "anime dark fantasy illustration, young swordsman descending a spiral stone staircase into ancient subterranean catacombs, "
        "holding a burning torch, eerie glowing crystals on cavern walls",
        1152, 648
    ),
    "escena_c2_e2.jpg": (
        "anime dark fantasy illustration, deep underground cavern with ancient stone altars and glowing sun runes carved into black obsidian rock, "
        "mysterious sacred sharpening stone resting on altar",
        1152, 648
    ),
    "escena_c2_e3.jpg": (
        "anime dark fantasy illustration, shadow rising from catacomb depths revealing six glowing red eyes in the darkness, "
        "terrifying demon aura, purple mist spreading across stone floor",
        1152, 648
    ),
    "escena_c3_e1.jpg": (
        "anime dark fantasy illustration, menacing six-eyed demon samurai drawing a long blade made of organic flesh and eyes, "
        "imposing posture, feudal purple kimono, terrifying power",
        1152, 648
    ),
    "escena_c3_e2.jpg": (
        "anime dark fantasy illustration, clash of crescent moon sword slashes and fiery sun breathing slashes in underground cavern, "
        "purple and orange sparks flying, high action manga battle",
        1152, 648
    ),
    "escena_c3_e3.jpg": (
        "anime dark fantasy illustration, young swordsman using transparent world perception seeing glowing red veins and muscles of demon opponent, "
        "x-ray tactical vision, dark fantasy manga effect",
        1152, 648
    ),
    "escena_c4_e1.jpg": (
        "anime dark fantasy illustration, young swordsman pressing his red-hot katana against an ancient sun sharpening stone, "
        "intense golden light burst, blade turning bright ruby red, epic forging moment",
        1152, 648
    ),
    "escena_c4_e2.jpg": (
        "anime dark fantasy illustration, young swordsman emerging from catacombs holding his newly perfected ruby katana, "
        "sunlight breaking through cavern entrance, heroic stance",
        1152, 648
    ),
    "escena_c4_e3.jpg": (
        "anime dark fantasy illustration, master leader of Demon Slayer corps sitting calmly in traditional Japanese room, "
        "knowing the demon lord is approaching, peaceful tragic atmosphere",
        1152, 648
    ),
    "escena_c5_e1.jpg": (
        "anime dark fantasy illustration, pale demon king stepping through sliding doors into the Master's sanctuary, "
        "red eyes glowing, dark aura engulfing the tatami room",
        1152, 648
    ),
    "escena_c5_e2.jpg": (
        "anime dark fantasy illustration, sudden fiery explosion destroying the entire mansion, "
        "sparks flying into midnight sky, demon lord caught in middle of blast",
        1152, 648
    ),
    "escena_c5_e3.jpg": (
        "anime dark fantasy illustration, endless shifting wooden rooms and upside-down staircases opening beneath falling warriors, "
        "descent into the Infinite Castle, epic cliffhanger wide shot",
        1152, 648
    )
}

print(f"\nGenerating all {len(prompts_vol6)} REAL AI images for Volume 6...")

for filename, (prompt, width, height) in prompts_vol6.items():
    out1 = vol6_dir1 / filename
    out2 = vol6_dir2 / filename
    print(f"[+] Generating Volume 6 illustration for {filename} ({width}x{height})...")
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

print("\nFinished generating all REAL AI images for Volume 6!")
