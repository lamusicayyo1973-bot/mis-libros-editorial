# -*- coding: utf-8 -*-
import sys
import os
import io
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

vol7_dir1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-7")
vol7_dir2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-7")

vol7_dir1.mkdir(parents=True, exist_ok=True)
vol7_dir2.mkdir(parents=True, exist_ok=True)

# 1. Delete old images in Volume 7
image_names = [
    "portada.jpg", "thumbnail.jpg", "banner.jpg", "escena_1.jpg", "escena_climax.jpg",
    "escena_c1_e1.jpg", "escena_c1_e2.jpg", "escena_c1_e3.jpg",
    "escena_c2_e1.jpg", "escena_c2_e2.jpg", "escena_c2_e3.jpg",
    "escena_c3_e1.jpg", "escena_c3_e2.jpg", "escena_c3_e3.jpg",
    "escena_c4_e1.jpg", "escena_c4_e2.jpg", "escena_c4_e3.jpg",
    "escena_c5_e1.jpg", "escena_c5_e2.jpg", "escena_c5_e3.jpg"
]

print("Clearing old images in Volume 7...")
for name in image_names:
    for folder in [vol7_dir1, vol7_dir2]:
        p = folder / name
        if p.exists():
            p.unlink()

print("Old images in Volume 7 deleted!")

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

# 3. Dedicated custom prompts for Volume 7: El Asedio al Castillo Infinito
prompts_vol7 = {
    "portada.jpg": (
        "anime dark fantasy manga cover art, young male swordsman with golden sun flame mark on forehead leaping through floating tatami rooms "
        "inside the infinite castle, upside down staircases, glowing ruby red katana, masterpiece",
        768, 1152
    ),
    "thumbnail.jpg": (
        "anime dark fantasy square thumbnail, pale demon with rainbow eyes and blonde hair holding golden lotus fans surrounded by ice flowers, "
        "vibrant colors, clean portrait, masterpiece manga style",
        768, 768
    ),
    "banner.jpg": (
        "anime dark fantasy wide banner, infinite castle architecture, endless floating wooden rooms and staircases extending into darkness, "
        "warriors fighting across platforms, masterpiece high quality manga style",
        1152, 648
    ),
    "escena_1.jpg": (
        "anime dark fantasy illustration, demon slayer warriors falling into the endless abyssal rooms of the shifting infinite castle, "
        "distorted gravity, biwa lute music echo, dramatic entrance shot",
        1152, 648
    ),
    "escena_climax.jpg": (
        "anime dark fantasy illustration, six-eyed demon samurai Kurogane disintegrating into glowing red ash after epic battle, "
        "broken flesh katana falling, stone pillars around him, emotional tragic victory, masterpiece manga style",
        1152, 648
    ),
    "escena_c1_e1.jpg": (
        "anime dark fantasy illustration, female insect Hashira in butterfly haori coat landing on upside down wooden beam inside infinite castle, "
        "holding stinger thin katana, dark purple lighting",
        1152, 648
    ),
    "escena_c1_e2.jpg": (
        "anime dark fantasy illustration, blonde demon with rainbow eyes smiling malevolently on a pile of lotus petals, "
        "holding two sharp golden lotus fans, ice mist floating",
        1152, 648
    ),
    "escena_c1_e3.jpg": (
        "anime dark fantasy illustration, butterfly female Hashira lunging forward with lightning speed thrusting her poisonous blade, "
        "purple butterfly aura around her, high action pose",
        1152, 648
    ),
    "escena_c2_e1.jpg": (
        "anime dark fantasy illustration, giant crystalline ice statues of Buddha emitting freezing frost aura, "
        "female swordsman surrounded by frost lotus flowers in temple room",
        1152, 648
    ),
    "escena_c2_e2.jpg": (
        "anime dark fantasy illustration, butterfly swordswoman sacrificing herself in a burst of purple wisteria poison mist, "
        "young female disciple screaming in grief drawing her sword, emotional dramatic scene",
        1152, 648
    ),
    "escena_c2_e3.jpg": (
        "anime dark fantasy illustration, young female disciple and boar-head warrior executing double blade decapitation against ice demon, "
        "shattering frost crystals, epic victory",
        1152, 648
    ),
    "escena_c3_e1.jpg": (
        "anime dark fantasy illustration, massive stone pillar warrior holding giant iron spiked ball and axe on chain, "
        "standing side by side with scar-faced wind pillar swordsman, facing dark hall",
        1152, 648
    ),
    "escena_c3_e2.jpg": (
        "anime dark fantasy illustration, six-eyed demon samurai drawing a massive dark flesh blade covered in glowing red eyes, "
        "crescent moon energy blades swirling around him",
        1152, 648
    ),
    "escena_c3_e3.jpg": (
        "anime dark fantasy illustration, young mist pillar swordsman pinned to stone pillar by demon blade, "
        "activating his demon slayer mark with burning rage",
        1152, 648
    ),
    "escena_c4_e1.jpg": (
        "anime dark fantasy illustration, stone pillar wielding spiked iron ball on chain smashing against crescent moon sword slashes, "
        "sparks flying, epic dark cavern battlefield",
        1152, 648
    ),
    "escena_c4_e2.jpg": (
        "anime dark fantasy illustration, wind pillar swordsman unleashing green tornado wind slashes alongside young sun swordsman's golden flame dragon, "
        "combined ultimate attack",
        1152, 648
    ),
    "escena_c4_e3.jpg": (
        "anime dark fantasy illustration, six-eyed demon samurai transforming into monstrous form with spiky bone blades erupting from his body, "
        "terrifying power unleash",
        1152, 648
    ),
    "escena_c5_e1.jpg": (
        "anime dark fantasy illustration, four warriors driving three glowing red katanas and an iron spike into the chest of the six-eyed demon, "
        "red solar light burning his flesh, climax battle",
        1152, 648
    ),
    "escena_c5_e2.jpg": (
        "anime dark fantasy illustration, six-eyed demon seeing his human Reflection in a broken blade, "
        "remembering his twin brother under a quiet sunset, peaceful tragic memory",
        1152, 648
    ),
    "escena_c5_e3.jpg": (
        "anime dark fantasy illustration, infinite castle rooms crumbling into dust as the structure rises to the surface, "
        "first rays of dawn appearing on the horizon, final battlefield transition",
        1152, 648
    )
}

print(f"\nGenerating all {len(prompts_vol7)} REAL AI images for Volume 7...")

for filename, (prompt, width, height) in prompts_vol7.items():
    out1 = vol7_dir1 / filename
    out2 = vol7_dir2 / filename
    print(f"[+] Generating Volume 7 illustration for {filename} ({width}x{height})...")
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

print("\nFinished generating all REAL AI images for Volume 7!")
