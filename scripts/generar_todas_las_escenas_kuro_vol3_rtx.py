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

KURO_VOL3_PROMPTS = [
    ("escena_c1_e1.jpg", "Anime style, dark fantasy manga illustration, three young protagonists standing on the deck of a wooden ship sailing across a silver liquid sea, glowing starry reflection, dark stormy continent in the distance, dramatic lighting, G-pen ink style, 8k"),
    ("escena_c1_e2.jpg", "Anime style, epic fantasy action shot, protagonist leaping in the air crossing his hands emitting black, white, and golden energy trails, destroying a giant crystal sea dragon on a silver ocean, ship in distress below, dynamic angles, manga line art"),
    ("escena_c1_e3.jpg", "Anime style, dark fantasy environment, three protagonists standing on a black sand beach looking up at colossal ancient statues of four-eyed beings, massive towering spire in the background emitting crimson light, atmospheric composition, detailed G-pen shading"),
    ("escena_c2_e1.jpg", "Anime style, dark fantasy interior, massive archive hall with floating liquid glass shelves and glowing memory orbs, ancient entity with three floating golden masks standing on a runic pedestal, three protagonists watching in tension, epic scale"),
    ("escena_c2_e2.jpg", "Anime style, dramatic revelation scene, 3D magical projection of an ancient war between magical civilizations, starry sky visible through a transparent ceiling with thousands of red falling stars, shock on character faces, detailed manga art"),
    ("escena_c2_e3.jpg", "Anime style, dark fantasy combat scene, alien invaders with organic armor and crystal wings attacking inside an archive tower, male protagonist summoning a massive wave of silver and black ink from the floor, dynamic action pose, G-pen manga style"),
    ("escena_c3_e1.jpg", "Anime style, dark fantasy magic spell, ancient entity dissolving into particles of light while touching the protagonist's forehead, thousands of memory orbs raining down as light spears, enemies turned to stone, emotional impact, high detail"),
    ("escena_c3_e2.jpg", "Anime style, character empowerment moment, protagonist with galaxy-like runic eyes looking at his two siblings with complete clarity and confidence, glowing aura of triple energy, heroic stance, detailed character design, manga artwork"),
    ("escena_c3_e3.jpg", "Anime style, epic fantasy climax setup, three protagonists standing on the roof of a tower facing hundreds of alien ships in the sky, massive pillars of silver ink forming a cosmic portal, breathtaking scale, cinematic framing, G-pen line art"),
    ("escena_c4_e1.jpg", "Anime style, dark fantasy urban battle, three protagonists arriving in a dark volcanic city made of black iron spires, surrounded by legions of armored alien soldiers, glowing red lava in the background, high action setup, detailed manga art"),
    ("escena_c4_e2.jpg", "Anime style, intense villain reveal, massive king in obsidian armor holding a glowing red relic on a volcanic throne, protagonist on one knee absorbing the pressure with a calm expression, high contrast lighting, G-pen style"),
    ("escena_c4_e3.jpg", "Anime style, dramatic victory scene, massive wave of multi-colored emotional energy restoring a dark city, giant villain's armor crumbling, protagonist holding a glowing iron quill in a calm stance, breathtaking visual impact, detailed line art"),
    ("escena_c5_e1.jpg", "Anime style, grand final celebration scene, three protagonists standing atop a tall white tower looking out over a newly merged continent with lush green fields and silver ocean under a clear blue sky, throwing magical weapons into the sea, peaceful and epic atmosphere"),
    ("escena_c5_e2.jpg", "Anime style, heartwarming epilogue, protagonist sitting under a golden-leaf tree writing in a notebook, children playing with colorful ink in the background, peaceful city rebuild, warm sunlight, emotional resolution, detailed character illustration"),
    ("escena_c5_e3.jpg", "Anime style, cinematic trilogy finale, male protagonist and silver-haired sister standing side by side on a green hill overlooking a vast new world at sunset, book in hand, inspiring and emotional closure, masterpiece manga artwork")
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
    kuro3_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\kuro-no-kineki-volumen-3"
    print("=== RENDERING KURO NO KINEKI VOL 3 LOCAL IMAGES ===")
    render_batch(KURO_VOL3_PROMPTS, kuro3_dir)
    print("=== KURO NO KINEKI VOL 3 LOCAL IMAGES GENERATED SUCCESSFULLY ON RTX 3060! ===")
