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

KURO_VOL2_PROMPTS = [
    ("escena_c1_e1.jpg", "Anime style, dark fantasy manga illustration, two protagonists holding glowing daggers standing on a cracked marble staircase, dark eclipsed sky over a futuristic floating city, giant dark crystal throne in the background, high contrast shadows, G-pen ink style, dramatic angle"),
    ("escena_c1_e2.jpg", "Anime style, intense emotional confrontation scene, knight in cracked golden armor standing between a supreme empress on a throne and two rebels with dark daggers, dramatic lighting, detailed character expressions, Japanese manga style, epic story moment"),
    ("escena_c1_e3.jpg", "Anime style, dark fantasy action transformation, young knight absorbed by golden magical energy, a golden glowing dagger emerging from his chest, dark empress controlling him like a puppet, two protagonists charging forward, epic composition, dynamic motion blur"),
    ("escena_c2_e1.jpg", "Anime style, high-speed sword fight, dark protagonist with glowing black dagger clashing against a golden-armored warrior with a flaming golden dagger, silver-haired girl throwing magical ink needles from the shadows, sparks flying, cinematic fight scene"),
    ("escena_c2_e2.jpg", "Anime style, emotional climax scene, protagonist on his knees absorbing golden corruption energy from his brother, brother handing him a glowing golden dagger with a desperate expression, silver-haired girl watching in shock, dramatic lighting, detailed character art"),
    ("escena_c2_e3.jpg", "Anime style, epic power awakening, male protagonist wielding two contrasting daggers (black ink and golden light), silver-haired girl touching his shoulder adding a white dagger, triple runic eye glowing, massive aura of swirling black, white, and gold energy, G-pen manga art"),
    ("escena_c3_e1.jpg", "Anime style, dark fantasy disaster scene, floating city tilting severely in the sky, huge chunks of marble falling through clouds, protagonists looking over the edge, massive glowing dark core suspended above a throne with a frozen figure inside, epic scale"),
    ("escena_c3_e2.jpg", "Anime style, dark fantasy reveal scene, empress projection transforming into a terrifying crystal monster with multiple sharp limbs, glowing dark core with a sleeping woman inside in the background, shock and horror on protagonists' faces, dramatic manga lighting"),
    ("escena_c3_e3.jpg", "Anime style, emotional sacrifice moment, male protagonist smiling softly at his silver-haired sister while holding three combined glowing weapons, sister crying and reaching out to him, crumbling palace background, swirling energy particles, G-pen manga art"),
    ("escena_c4_e1.jpg", "Anime style, epic climactic action, protagonist plunging three glowing daggers into a massive dark core, explosion of multi-colored energy, cracks glowing on protagonist's skin, floating city descending gently through clouds, breathtaking visual scale"),
    ("escena_c4_e2.jpg", "Anime style, dark fantasy aftermath, crystal empress crumbling into dust, sleeping mother rescued by silver-haired girl and golden knight, quiet atmosphere, debris floating in the air, sunset light breaking through clouds, detailed manga line art"),
    ("escena_c4_e3.jpg", "Anime style, heartbreaking emotional scene, protagonist with glowing white empty eyes smiling melancholy at his brother and sister, shadowy ink particles floating off his body, sunset background over the newly grounded city, high emotional impact, detailed character art"),
    ("escena_c5_e1.jpg", "Anime style, hopeful dark fantasy aftermath, giant white city grounded on a green fertile valley, former enemies working together rebuilding, bright blue sky, peaceful atmosphere, cinematic wide shot, detailed environment art"),
    ("escena_c5_e2.jpg", "Anime style, peaceful ending scene, protagonist with a travel coat and runic eye sitting on a grassy cliff alongside his silver-haired sister, looking over a vast new world at sunset, warm color palette, emotional closure, G-pen line art"),
    ("escena_c5_e3.jpg", "Anime style, mysterious cliffhanger ending, protagonist standing on a cliff at dusk looking toward a distant dark tower glowing across the ocean, glowing rune on his palm, ominous dark clouds in the far distance, epic setup for future adventures")
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
    kuro2_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\kuro-no-kineki-volumen-2"
    print("=== RENDERING KURO NO KINEKI VOL 2 LOCAL IMAGES ===")
    render_batch(KURO_VOL2_PROMPTS, kuro2_dir)
    print("=== KURO NO KINEKI VOL 2 LOCAL IMAGES GENERATED SUCCESSFULLY ON RTX 3060! ===")
