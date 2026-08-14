# -*- coding: utf-8 -*-
import sys
import os
import io
import torch
from pathlib import Path
from diffusers import StableDiffusionXLPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

vol9_dir1 = Path(r"C:\Proyectos\mis-libros-editorial\libros\oni-no-ketsuryu-volumen-9")
vol9_dir2 = Path(r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-9")

vol9_dir1.mkdir(parents=True, exist_ok=True)
vol9_dir2.mkdir(parents=True, exist_ok=True)

# 1. Delete old images in Volume 9
image_names = [
    "portada.jpg", "thumbnail.jpg", "banner.jpg", "escena_1.jpg", "escena_climax.jpg",
    "escena_c1_e1.jpg", "escena_c1_e2.jpg", "escena_c1_e3.jpg",
    "escena_c2_e1.jpg", "escena_c2_e2.jpg", "escena_c2_e3.jpg",
    "escena_c3_e1.jpg", "escena_c3_e2.jpg", "escena_c3_e3.jpg",
    "escena_c4_e1.jpg", "escena_c4_e2.jpg", "escena_c4_e3.jpg",
    "escena_c5_e1.jpg", "escena_c5_e2.jpg", "escena_c5_e3.jpg"
]

print("Clearing old images in Volume 9...")
for name in image_names:
    for folder in [vol9_dir1, vol9_dir2]:
        p = folder / name
        if p.exists():
            p.unlink()

print("Old images in Volume 9 deleted!")

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

# 3. Dedicated custom prompts for Volume 9: La Noche de los Noventa Minutos
prompts_vol9 = {
    "portada.jpg": (
        "anime dark fantasy manga cover art, young swordsman with glowing sun mark unleashing the 13th Solar Dance Form, "
        "flaming solar wheel around his red katana, fighting demon lord on ruined city streets, masterpiece",
        768, 1152
    ),
    "thumbnail.jpg": (
        "anime dark fantasy square thumbnail, pale demon lord Kageyama with red glowing eyes and black whip tentacles erupting from his back, "
        "vibrant colors, intense villain portrait, masterpiece manga style",
        768, 768
    ),
    "banner.jpg": (
        "anime dark fantasy wide banner, ruined city street under midnight sky, rubble burning, "
        "warriors of the solar brotherhood charging against demon lord, cinematic wide shot, masterpiece",
        1152, 648
    ),
    "escena_1.jpg": (
        "anime dark fantasy illustration, demon lord Kageyama standing in middle of cratered town square at night, "
        "black whip tentacles tearing through buildings, terrifying red aura",
        1152, 648
    ),
    "escena_climax.jpg": (
        "anime dark fantasy illustration, golden rays of morning sun breaking over mountain peaks, "
        "hitting a giant demon flesh monster pinned by a radiant solar katana, disintegrating into light sparks, masterpiece climax",
        1152, 648
    ),
    "escena_c1_e1.jpg": (
        "anime dark fantasy illustration, injured warriors of the brotherhood crawling out of collapsed masonry rubble in city streets, "
        "drawing katanas under full moon",
        1152, 648
    ),
    "escena_c1_e2.jpg": (
        "anime dark fantasy illustration, demon lord whipping sharp black spine tentacles at hypersonic speed, "
        "slicing stone buildings in half, high action scene",
        1152, 648
    ),
    "escena_c1_e3.jpg": (
        "anime dark fantasy illustration, cat demon medicine bearer tossing glowing vials of antidote to injured warriors on rooftops, "
        "mysterious night scene",
        1152, 648
    ),
    "escena_c2_e1.jpg": (
        "anime dark fantasy illustration, demon lord coughing black blood in shock as Sumire's aging drug rapidly turns his dark hair white, "
        "weakening demonic cells",
        1152, 648
    ),
    "escena_c2_e2.jpg": (
        "anime dark fantasy illustration, blind stone warrior and scarred wind warrior launching relentless assault with iron spiked ball and wind slashes, "
        "buying time in the street",
        1152, 648
    ),
    "escena_c2_e3.jpg": (
        "anime dark fantasy illustration, young swordsman Ren kneeling panting on ground, memories of his ancestors filling his mind, "
        "sun mark glowing brighter",
        1152, 648
    ),
    "escena_c3_e1.jpg": (
        "anime dark fantasy illustration, young swordsman standing up executing continuous wheel of fiery solar slashes, "
        "twelve solar dance forms flowing into one continuous flaming dragon",
        1152, 648
    ),
    "escena_c3_e2.jpg": (
        "anime dark fantasy illustration, demon lord's whip tentacles clashing against golden solar wheel slashes, "
        "intense sparks and fire particles",
        1152, 648
    ),
    "escena_c3_e3.jpg": (
        "anime dark fantasy illustration, giant grandfather clock face appearing in night sky showing 15 minutes to sunrise, "
        "dramatic countdown visual, dark manga art style",
        1152, 648
    ),
    "escena_c4_e1.jpg": (
        "anime dark fantasy illustration, demon lord Kageyama swelling into a massive hideous fleshy giant infant monster to block the sunlight, "
        "grotesque dark fantasy form",
        1152, 648
    ),
    "escena_c4_e2.jpg": (
        "anime dark fantasy illustration, giant flesh demon monster trying to dig into the ground to escape, "
        "warriors holding iron chains pulling him back into the open",
        1152, 648
    ),
    "escena_c4_e3.jpg": (
        "anime dark fantasy illustration, young swordsman driving his ruby red katana deep into the giant demon's heart, "
        "holding blade with both hands as sun crests the horizon",
        1152, 648
    ),
    "escena_c5_e1.jpg": (
        "anime dark fantasy illustration, bright golden sunlight touching the skin of the giant demon monster, "
        "cracks of light spreading across his body, disintegrating into glowing ash",
        1152, 648
    ),
    "escena_c5_e2.jpg": (
        "anime dark fantasy illustration, demon lord's consciousness dissolving into dark void, "
        "realizing his eternal quest for perfection has failed, dramatic villain end",
        1152, 648
    ),
    "escena_c5_e3.jpg": (
        "anime dark fantasy illustration, quiet dawn breaking over peaceful ruined city, "
        "sunlight illuminating victorious exhausted warriors resting on stone steps",
        1152, 648
    )
}

print(f"\nGenerating all {len(prompts_vol9)} REAL AI images for Volume 9...")

for filename, (prompt, width, height) in prompts_vol9.items():
    out1 = vol9_dir1 / filename
    out2 = vol9_dir2 / filename
    print(f"[+] Generating Volume 9 illustration for {filename} ({width}x{height})...")
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

print("\nFinished generating all REAL AI images for Volume 9!")
