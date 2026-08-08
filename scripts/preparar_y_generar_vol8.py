# -*- coding: utf-8 -*-
import sys
import os
import io
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

vol8_dir1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-8")
vol8_dir2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-8")

vol8_dir1.mkdir(parents=True, exist_ok=True)
vol8_dir2.mkdir(parents=True, exist_ok=True)

# 1. Delete old images in Volume 8
image_names = [
    "portada.jpg", "thumbnail.jpg", "banner.jpg", "escena_1.jpg", "escena_climax.jpg",
    "escena_c1_e1.jpg", "escena_c1_e2.jpg", "escena_c1_e3.jpg",
    "escena_c2_e1.jpg", "escena_c2_e2.jpg", "escena_c2_e3.jpg",
    "escena_c3_e1.jpg", "escena_c3_e2.jpg", "escena_c3_e3.jpg",
    "escena_c4_e1.jpg", "escena_c4_e2.jpg", "escena_c4_e3.jpg",
    "escena_c5_e1.jpg", "escena_c5_e2.jpg", "escena_c5_e3.jpg"
]

print("Clearing old images in Volume 8...")
for name in image_names:
    for folder in [vol8_dir1, vol8_dir2]:
        p = folder / name
        if p.exists():
            p.unlink()

print("Old images in Volume 8 deleted!")

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

# 3. Dedicated custom prompts for Volume 8: El Juicio de los Tres Demonios del Abismo
prompts_vol8 = {
    "portada.jpg": (
        "anime dark fantasy manga cover art, martial artist demon with blue tattoos and pink hair standing inside a giant blue glowing snowflake compass, "
        "facing a young swordsman with a fiery red katana, epic confrontation, masterpiece",
        768, 1152
    ),
    "thumbnail.jpg": (
        "anime dark fantasy square thumbnail, martial artist demon Punching forward with shockwaves of blue martial aura, "
        "vibrant blue energy, intense eyes, masterpiece manga style",
        768, 768
    ),
    "banner.jpg": (
        "anime dark fantasy wide banner, martial art arena inside infinite castle, blue snowflake compass glowing on tatami floor, "
        "shockwaves radiating outwards, masterpiece high quality manga art style",
        1152, 648
    ),
    "escena_1.jpg": (
        "anime dark fantasy illustration, martial artist demon Rikudo unleashing Annihilation Type shockwaves with glowing blue fists, "
        "young swordsman deflecting blows with flame blade, high action manga scene",
        1152, 648
    ),
    "escena_climax.jpg": (
        "anime dark fantasy illustration, demon king Kageyama bursting out of a fleshy cocoon on city rooftops under full moon, "
        "black whip tentacles spreading, terrifying dark overlord, masterpiece climax shot",
        1152, 648
    ),
    "escena_c1_e1.jpg": (
        "anime dark fantasy illustration, young swordsman entering state of selfless intent, aura disappearing, "
        "invisible to demon's compass perception, tactical battle moment",
        1152, 648
    ),
    "escena_c1_e2.jpg": (
        "anime dark fantasy illustration, clean decapitation strike of martial artist demon by a glowing solar red blade, "
        "blue compass shattering like glass, golden embers flying",
        1152, 648
    ),
    "escena_c1_e3.jpg": (
        "anime dark fantasy illustration, headless demon body trying to regenerate its head through sheer willpower, "
        "scary demonic muscle surge, dark purple energy",
        1152, 648
    ),
    "escena_c2_e1.jpg": (
        "anime dark fantasy illustration, spiritual vision of a young human martial artist embracing his fiancee under romantic Japanese festival fireworks, "
        "tearful human memory, emotional contrast",
        1152, 648
    ),
    "escena_c2_e2.jpg": (
        "anime dark fantasy illustration, demon Rikudo striking himself with his own fists in self-redemption, "
        "disintegrating peacefully into golden sparks, emotional farewell",
        1152, 648
    ),
    "escena_c2_e3.jpg": (
        "anime dark fantasy illustration, ice demon Kagura absorbing poison wisteria, his skin melting away with purple veins, "
        "shocked expression, crumbling ice temple background",
        1152, 648
    ),
    "escena_c3_e1.jpg": (
        "anime dark fantasy illustration, young female swordswoman executing final butterfly slash slicing through ice demon's neck, "
        "purple and blue butterfly wings aura surrounding the blade",
        1152, 648
    ),
    "escena_c3_e2.jpg": (
        "anime dark fantasy illustration, boar-head warrior crying while holding his serrated dual katanas over defeated ice demon ashes, "
        "emotional battle aftermath",
        1152, 648
    ),
    "escena_c3_e3.jpg": (
        "anime dark fantasy illustration, stone pillar and wind pillar standing together facing six-eyed demon Kurogane in ruined temple hall, "
        "dust clearing, dramatic standoff",
        1152, 648
    ),
    "escena_c4_e1.jpg": (
        "anime dark fantasy illustration, six-eyed demon samurai unleashing crescent moon sword blades flying across cavern, "
        "stone pillars slicing into pieces, high action dark fantasy",
        1152, 648
    ),
    "escena_c4_e2.jpg": (
        "anime dark fantasy illustration, three swordsmen clashing katanas together turning their blades white-hot radiant red, "
        "intense heat waves, fiery dragon aura",
        1152, 648
    ),
    "escena_c4_e3.jpg": (
        "anime dark fantasy illustration, four red blades impaling six-eyed demon, solar fire burning his flesh, "
        "demon's eyes glowing red in agony",
        1152, 648
    ),
    "escena_c5_e1.jpg": (
        "anime dark fantasy illustration, six-eyed demon samurai disintegrating into dust, leaving behind a small wooden flute on tatami floor, "
        "tragic ancient memory",
        1152, 648
    ),
    "escena_c5_e2.jpg": (
        "anime dark fantasy illustration, demon king Kageyama breaking out of flesh cocoon in town square at night, "
        "black spine whips extending, 90 minute countdown to dawn starting",
        1152, 648
    ),
    "escena_c5_e3.jpg": (
        "anime dark fantasy illustration, surviving Sables de Elite pillars assembling on city street under full moon, "
        "drawing katanas for final 90-minute battle against Demon King",
        1152, 648
    )
}

print(f"\nGenerating all {len(prompts_vol8)} REAL AI images for Volume 8...")

for filename, (prompt, width, height) in prompts_vol8.items():
    out1 = vol8_dir1 / filename
    out2 = vol8_dir2 / filename
    print(f"[+] Generating Volume 8 illustration for {filename} ({width}x{height})...")
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

print("\nFinished generating all REAL AI images for Volume 8!")
