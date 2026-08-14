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

fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"

pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")

print("[+] Generando escena_c5_e3.jpg en puro estilo anime 2D...")
image = pipe(
    prompt=(
        "2d anime dark fantasy manga illustration, handsome young adult samurai Ren with dark hair in black kimono "
        "and beautiful maiden Miyuki with long dark hair in pink kimono walking together on stone path under cherry blossom trees in mountain village, "
        "vibrant anime art style, masterpiece, 2d drawing"
    ),
    negative_prompt="photorealistic, photo, real person, photograph, realistic photography, 3d render, live action, lowres, blurry, ugly",
    num_inference_steps=28,
    guidance_scale=8.5,
    width=1152,
    height=648
).images[0]

image.save(vol10_dir1 / "escena_c5_e3.jpg")
image.save(vol10_dir2 / "escena_c5_e3.jpg")
print("Guardada escena_c5_e3.jpg en puro estilo anime 2D!")
