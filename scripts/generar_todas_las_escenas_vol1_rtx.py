import os
os.environ["XFORMERS_PACKAGE_IS_DISABLED"] = "1"
os.environ["XFORMERS_DISABLED"] = "1"

import sys
import torch
from diffusers import StableDiffusionXLPipeline

ckpt_path = r"C:\pinokio\api\fooocus.git\app\models\checkpoints\juggernautXL_v8Rundiffusion.safetensors"

print(f"Loading local SDXL pipeline on RTX 3060 from {ckpt_path}...")
pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe.to("cuda")
print("Pipeline loaded successfully on CUDA GPU!")

VOL1_PROMPTS = [
    ("escena_c1_e1.jpg", "Anime style, dark fantasy manga illustration, a young male blacksmith with messy black hair hammering glowing hot steel in a traditional Japanese forge, winter snow outside the wooden workshop, warm fire lighting, G-pen ink style, highly detailed"),
    ("escena_c1_e2.jpg", "Anime style, dramatic dark fantasy scene, giant four-horned demon with glowing yellow eyes invading a traditional Japanese house, young protagonist holding an unfinished katana in shock, snowing blizzard background, high contrast shadows, intense action"),
    ("escena_c1_e3.jpg", "Anime style, dark fantasy awakening, young protagonist with black marks spreading on his face holding a glowing broken katana made of black crystal and red energy, fighting a giant horned demon, dramatic lighting, G-pen manga art"),
    ("escena_c2_e1.jpg", "Anime style, emotional dark fantasy scene, male protagonist reaching out to his young sister who has glowing slit eyes and small horns, snowy background, intense emotional facial expressions, detailed anime character art"),
    ("escena_c2_e2.jpg", "Anime style, character design shot, anime girl with a bamboo gag in her mouth wearing a kimono and cloak, holding her brother's hand in the snow, young swordsman with black hair and face marks holding a sheath, atmospheric winter mood"),
    ("escena_c2_e3.jpg", "Anime style, sword clash action scene, dark protagonist blocking a crimson katana with his broken dark sword, demon hunter wearing a Tengu raven mask in a blue haori, snowing mountain background, dynamic camera angle, high tension"),
    ("escena_c3_e1.jpg", "Anime style, dramatic stand-off, anime girl standing in front of her brother protecting him, raven-masked hunter sheathing his crimson sword, snowy landscape at twilight, emotional tension, detailed manga art"),
    ("escena_c3_e2.jpg", "Anime style, dark fantasy travel shot, protagonist carrying a large woven basket covered with cloth on his back, climbing a steep rocky mountain during sunrise, exhausted expression, scenic mountain views, G-pen shading"),
    ("escena_c3_e3.jpg", "Anime style, peaceful master and student scene, young protagonist bowing deeply to a scarred veteran swordsman sitting on a wooden porch surrounded by purple wisteria flowers, basket on the side, anime aesthetic"),
    ("escena_c4_e1.jpg", "Anime style, training montage, protagonist dodging wooden traps in a dark forest with blindfolds, sword swings creating air shockwaves, glowing black marks on his arms, high action intensity, G-pen line art"),
    ("escena_c4_e2.jpg", "Anime style, epic samurai action shot, young swordsman unleashing a flaming red sword strike on a massive boulder, the boulder splitting in half with glowing cracks, sakura and wisteria petals flying in the wind, dramatic lighting"),
    ("escena_c4_e3.jpg", "Anime style, departure scene, protagonist wearing a new black haori with red patterns standing next to his sister and mentor on a mountain cliff, sunset horizon, epic journey setup, detailed character artwork"),
    ("escena_c5_e1.jpg", "Anime style, dark fantasy entrance scene, dozens of young swordsmen gathered in front of a massive wooden gate surrounded by glowing purple wisteria trees at night, eerie atmosphere, detailed crowd art"),
    ("escena_c5_e2.jpg", "Anime style, terrifying dark fantasy encounter, giant grotesque monster covered in multiple arms emerging from a dark forest, young protagonist drawing his black flaming katana, high contrast lighting, dark fantasy aesthetic"),
    ("escena_c5_e3.jpg", "Anime style, epic climax scene, young swordsman delivering a rotating spiral red flame strike toward a giant multi-armed monster, defeated enemy dissolving into light particles, glowing sunrise behind purple wisteria flowers, masterpiece manga artwork")
]

def render_batch(prompts_list, target_dir):
    os.makedirs(target_dir, exist_ok=True)
    for filename, prompt in prompts_list:
        out_path = os.path.join(target_dir, filename)
        print(f"Rendering local image on RTX 3060: {target_dir}/{filename}...")
        img = pipe(
            prompt=prompt,
            negative_prompt="low quality, blurry, worst quality, deformed, text watermark",
            num_inference_steps=20,
            guidance_scale=7.5,
            width=1024,
            height=576
        ).images[0]
        img.save(out_path)
        print(f"Saved -> {out_path}")

if __name__ == "__main__":
    v1_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-1"
    print("=== RENDERING VOL 1 LOCAL IMAGES ===")
    render_batch(VOL1_PROMPTS, v1_dir)
    print("=== VOL 1 LOCAL IMAGES GENERATED SUCCESSFULLY ON RTX 3060! ===")
