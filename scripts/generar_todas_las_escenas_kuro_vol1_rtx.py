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

KURO_VOL1_PROMPTS = [
    ("escena_c1_e1.jpg", "Anime style, dark fantasy manga illustration, a young male protagonist with messy black hair and white streak, glowing white runic eye, holding a dark iron dagger, standing on bronze ruins, surrounded by black ink fog and dissolving stone guardian, dramatic lighting, highly detailed, G-pen ink style, 8k"),
    ("escena_c1_e2.jpg", "Anime style, dark fantasy manga action shot, giant bronze clockwork automaton with four arms attacking a young warrior, protagonist stabbing his arm with a dagger emitting dark flaming ink, dynamic motion blur, high contrast shadows, Japanese manga aesthetics, epic encounter"),
    ("escena_c1_e3.jpg", "Anime style, dramatic confrontation, a young woman with long silver hair and white ceremonial robes holding a dark glowing dagger, facing a black-haired protagonist holding a silver locket, moonlit underground ruins background, intense atmosphere, detailed anime character design, highly stylized"),
    ("escena_c2_e1.jpg", "Anime style, dark fantasy manga, intense dialogue scene between a young male warrior with black hair and white streaks and a young woman with silver hair in white robes, illuminated by glowing runes, dark underground ruins background, high contrast shadows, Japanese manga aesthetic, emotional tension, detailed character designs"),
    ("escena_c2_e2.jpg", "Anime style, dark fantasy manga environment, two anime characters running through a dark steampunk underground tunnel with massive copper pipes and glowing black fluid, creepy glowing white eyes emerging from the shadows ahead, ominous atmosphere, cinematic composition, manga line art"),
    ("escena_c2_e3.jpg", "Anime style, dynamic dark fantasy battle scene, protagonist touching the chest of a dark shadow monster causing it to dissolve into glowing black ink particles, runic eye glowing brightly, silver-haired girl in the background looking shocked, action pose, dramatic lighting, G-pen manga style, intense impact"),
    ("escena_c3_e1.jpg", "Anime style, dark fantasy manga, protagonist on his knees clutching his head in pain, glowing red-to-white runic eye, silver-haired girl standing nearby looking at him with awe and fear, dark underground catacombs background, glowing dust particles, moody lighting, highly detailed manga art"),
    ("escena_c3_e2.jpg", "Anime style, dark fantasy manga cityscape, massive underground slum built inside a cavern, wooden bridges, copper pipes, dimly lit lanterns, shadowy impoverished crowds walking below, two hooded protagonists looking over the city from a ledge, atmospheric perspective, G-pen shading"),
    ("escena_c3_e3.jpg", "Anime style, dark fantasy manga climax scene, a terrifying knight in white armor and a featureless porcelain mask holding a massive golden greatsword, standing atop a huge iron gate, facing two young protagonists with glowing dark daggers below, dramatic low-angle shot, epic tension"),
    ("escena_c4_e1.jpg", "Anime style, dark fantasy action scene, knight in white armor swinging a massive glowing golden broadsword creating a wave of golden light, protagonist blocking the attack with a dark violet flaming dagger, shockwave debris, high contrast, dynamic angles, manga line art"),
    ("escena_c4_e2.jpg", "Anime style, dark fantasy dramatic moment, protagonist shattering a featureless porcelain mask with a black flaming dagger, revealing the face of a young man who looks shockingly similar to the protagonist, broken mask pieces flying, high tension, detailed facial expressions, G-pen style"),
    ("escena_c4_e3.jpg", "Anime style, dark fantasy cliffhanger, a giant beam of golden light ascending into the ceiling carrying away the defeated knight, two protagonists standing in front of the glowing portal residue, dark atmosphere, epic scale, cinematic framing, manga artwork"),
    ("escena_c5_e1.jpg", "Anime style, epic dark fantasy manga splash page, two protagonists emerging from a beam of light onto a majestic floating city made of white marble and crystal spires, clouds below, giant dark pipes siphoning ink from the abyss, breathtaking contrast between heavenly architecture and dark energy, highly detailed manga art"),
    ("escena_c5_e2.jpg", "Anime style, dark fantasy dramatic confrontation, supreme empress sitting on a floating throne above a marble staircase, holding a dark glowing orb of memories, defeated golden knight on her side, two shocked protagonists below, grand throne room, intricate details, G-pen manga style"),
    ("escena_c5_e3.jpg", "Anime style, dark fantasy manga volume finale, two protagonists charging up a grand marble staircase with crossed glowing daggers, creating a massive wave of black and white ink energy, dark eclipsed sky background, empress standing up from throne in shock, epic climax, dynamic motion, G-pen line art")
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
    kuro1_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\kuro-no-kineki-volumen-1"
    print("=== RENDERING KURO NO KINEKI VOL 1 LOCAL IMAGES ===")
    render_batch(KURO_VOL1_PROMPTS, kuro1_dir)
    print("=== KURO NO KINEKI VOL 1 LOCAL IMAGES GENERATED SUCCESSFULLY ON RTX 3060! ===")
