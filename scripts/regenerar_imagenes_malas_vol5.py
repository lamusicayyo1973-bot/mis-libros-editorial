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
    "mask, surgical mask, face mask, covid mask, modern clothes, t-shirt, jeans, robot, "
    "mecha, plastic doll, toy figure, 3d render, photorealistic photo, bamboo robot, "
    "wooden robot, western, lowres, blurry, ugly, watermark, text, logo, bad anatomy"
)

print(f"Loading SDXL Pipeline from {ckpt_path} on GPU...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

# Only regenerate the 8 bad images with corrected, very specific prompts
prompts_corregidos = {
    "escena_c1_e1.jpg": (
        "anime dark fantasy illustration, young japanese swordsman with a flame mark on his face "
        "arriving blindfolded at a hidden feudal village full of hot springs and volcanic rocks, "
        "villagers wearing traditional Hyottoko festival wooden face masks with kimono, "
        "steam rising from hot springs, traditional wooden huts, torchlight, cinematic wide shot, "
        "masterpiece, high quality manga art style",
        1152, 648
    ),
    "escena_c1_e2.jpg": (
        "anime dark fantasy illustration, old swordsmith village chief with long white beard "
        "in traditional kimono presenting a giant six-armed training dummy made of wood and straw "
        "holding six wooden practice katanas in a misty bamboo clearing, "
        "torches lit around it, dramatic low angle view, feudal japan setting, masterpiece manga art",
        1152, 648
    ),
    "escena_c1_e3.jpg": (
        "anime dark fantasy illustration, smashed wooden training dummy falling apart "
        "revealing a hidden jet-black ancient katana with crimson handle glowing inside its torso, "
        "splinters flying, golden light emanating from the blade, feudal japan dojo background, "
        "dramatic close-up, masterpiece manga illustration style",
        1152, 648
    ),
    "escena_c3_e3.jpg": (
        "anime dark fantasy illustration, agile female swordsman with pink hair in traditional "
        "battle kimono leaping through the air slicing giant wooden dragon heads with a glowing "
        "pink flexible katana that bends like a whip, fire sparks, dramatic action pose, "
        "feudal japan forest background with moonlight, masterpiece manga art style",
        1152, 648
    ),
    "escena_c4_e1.jpg": (
        "anime dark fantasy illustration, a desperate swordsmith wearing a traditional Hyottoko "
        "wooden mask and leather apron running through a burning forge workshop, "
        "tossing a fully polished radiant sun-golden katana blade through the flames "
        "to a young swordsman waiting with outstretched hands, embers flying, "
        "feudal japan blacksmith setting, dramatic cinematic angle, masterpiece manga style",
        1152, 648
    ),
    "escena_c5_e1.jpg": (
        "anime dark fantasy illustration, exhausted battle-worn young swordsman in torn kimono "
        "kneeling on scorched grass at dawn, eyes wide open in shock and disbelief, "
        "looking toward his demonic sister standing in the morning sunlight unharmed, "
        "emotional dramatic scene, mist rising from the ground, feudal japan field, "
        "golden sunrise light, masterpiece manga illustration",
        1152, 648
    ),
    "escena_c5_e2.jpg": (
        "anime dark fantasy illustration, young demon girl in traditional feudal kimono "
        "gently removing a bamboo mouthpiece from her lips, smiling softly with relief, "
        "standing under warm golden morning sunlight that touches her skin without harm, "
        "tears in her eyes, emotional reunion moment, feudal japan setting, "
        "sakura petals in the wind, masterpiece manga art style",
        1152, 648
    ),
    "escena_climax.jpg": (
        "anime dark fantasy illustration, miraculous emotional scene at dawn, "
        "young teenage girl in feudal kimono standing in bright morning sunlight completely unharmed, "
        "her brother in battle-worn samurai clothes weeping with joy and embracing her, "
        "golden light rays, feudal japan forest, cherry blossoms falling, "
        "masterpiece high quality manga illustration emotional climax",
        1152, 648
    ),
}

print(f"\nRegenerando {len(prompts_corregidos)} imagenes corregidas para Volumen 5...\n")

for filename, (prompt, width, height) in prompts_corregidos.items():
    out1 = base_dir1 / filename
    out2 = base_dir2 / filename
    print(f"[+] Generando: {filename} ({width}x{height})...")
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
        print(f"    Guardada: {out1}")
    except Exception as e:
        print(f"    ERROR generando {filename}: {e}")

print("\nFinished regenerating all 8 corrected images for Volume 5!")
