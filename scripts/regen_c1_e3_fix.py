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
    "mask, surgical mask, face mask, modern clothes, t-shirt, jeans, robot, mecha, "
    "plastic doll, toy figure, 3d render, watermark, text, logo, "
    "extra arms, extra limbs, extra hands, three arms, mutant, deformed anatomy, "
    "bad anatomy, ugly, blurry, lowres"
)

print("Loading SDXL Pipeline...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

prompt = (
    "anime dark fantasy manga illustration, a young male swordsman in torn black kimono "
    "kneeling on a wooden dojo floor, holding a glowing jet-black ancient katana with two hands, "
    "the katana blade radiates crimson red light and embers, splinters of broken wood around him, "
    "dramatic low angle cinematic shot, feudal japan dojo interior, torch lighting, "
    "two arms only, correct human anatomy, masterpiece high quality manga art"
)

filename = "escena_c1_e3.jpg"
out1 = base_dir1 / filename
out2 = base_dir2 / filename

print(f"[+] Regenerando {filename} (sin brazos de mas)...")
image = pipe(
    prompt=prompt,
    negative_prompt=NEGATIVE,
    num_inference_steps=30,
    guidance_scale=8.5,
    width=1152,
    height=648
).images[0]

image.save(out1)
image.save(out2)
print(f"Guardada: {out1}")
print("Listo!")
