import os
os.environ["XFORMERS_PACKAGE_IS_DISABLED"] = "1"
os.environ["XFORMERS_DISABLED"] = "1"

import torch
from diffusers import StableDiffusionXLPipeline

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"

print(f"Loading SDXL checkpoint directly on RTX 3060: {ckpt_path}")

try:
    pipe = StableDiffusionXLPipeline.from_single_file(
        ckpt_path,
        torch_dtype=torch.float16,
        use_safetensors=True
    )
    pipe.to("cuda")
    print("Pipeline loaded successfully on CUDA GPU!")
    
    prompt = "Anime style, dark fantasy manga illustration, old retired swordsman presenting an ancient scroll book to a young black-haired protagonist with a flame-shaped face mark, traditional Japanese room with sliding doors at dusk, G-pen ink style, highly detailed"
    output_path = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-4\escena_c1_e1.jpg"
    
    print("Generating image on RTX 3060...")
    img = pipe(
        prompt=prompt,
        negative_prompt="low quality, blurry, worst quality, deformed, text watermark",
        num_inference_steps=20,
        guidance_scale=7.0,
        width=1024,
        height=576
    ).images[0]
    
    img.save(output_path)
    print(f"SUCCESSFULLY GENERATED & SAVED TO {output_path}")
except Exception as e:
    print("Error during direct SDXL generation:", e)
