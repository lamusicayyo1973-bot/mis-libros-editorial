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

VOL2_PROMPTS = [
    ("escena_c1_e1.jpg", "Anime style, dark fantasy manga illustration, four young swordsmen standing at the exit of a purple wisteria forest during sunrise, two mysterious porcelain-faced girls presenting a table with dark glowing ore blocks, G-pen ink style, highly detailed"),
    ("escena_c1_e2.jpg", "Anime style, character shot, young black-haired protagonist with black face marks, carrying a large wooden basket on his back, a black messenger raven with a bronze plate perched on his shoulder, scenic sunrise background, detailed manga art"),
    ("escena_c1_e3.jpg", "Anime style, detailed weapon reveal scene, young swordsman desheathing a jet-black katana with a glowing thin red line along the edge, eccentric blacksmith wearing a Hyottoko mask standing nearby, atmospheric lighting, G-pen line art"),
    ("escena_c2_e1.jpg", "Anime style, dark fantasy environment, young protagonist walking down a dark traditional Japanese alley illuminated by red paper lanterns, shadowy rooftops above, ominous atmosphere, high contrast shading"),
    ("escena_c2_e2.jpg", "Anime style, action encounter, swordsman fighting a giant monster made of glowing melted wax in a narrow alley, red paper lanterns background, dynamic poses, high intensity, G-pen manga style"),
    ("escena_c2_e3.jpg", "Anime style, dynamic tag-team action scene, anime girl with bamboo gag unleashing a kick surrounded by purple flames next to her brother holding a black glowing katana, fighting a wax monster, epic composition"),
    ("escena_c3_e1.jpg", "Anime style, epic swordsman finisher move, young protagonist unleashing a rotating red fire sword strike, monster dissolving into glowing red embers, night sky background, dramatic lighting, masterpiece art"),
    ("escena_c3_e2.jpg", "Anime style, emotional aftermath scene, anime girl with bamboo gag kneeling by glowing embers on a stone street, young swordsman standing beside her looking up at the moon, quiet mood, detailed manga illustration"),
    ("escena_c3_e3.jpg", "Anime style, mysterious villain cliffhanger, shadowy figure holding a traditional Japanese biwa lute sitting atop a clock tower at night, glowing eye mark, misty sky background, eerie composition"),
    ("escena_c4_e1.jpg", "Anime style, briefing scene, young swordsman listening to his messenger raven on a wooden inn balcony during sunrise, large wooden basket on the floor, scenic traditional Japanese village, G-pen shading"),
    ("escena_c4_e2.jpg", "Anime style, character introduction scene, powerful swordsman with spiky flame-colored hair wearing a flame-patterned haori eating enthusiastically inside a vintage train car, young protagonist looking surprised nearby"),
    ("escena_c4_e3.jpg", "Anime style, dramatic dialogue scene, powerful flame swordsman looking intently at the young protagonist inside a dimly lit train car, atmospheric lighting, high tension, detailed character designs"),
    ("escena_c5_e1.jpg", "Anime style, dark fantasy spell effect, pale train conductor punching tickets emitting glowing purple mist, passengers falling asleep in their seats inside a vintage train, eerie atmosphere"),
    ("escena_c5_e2.jpg", "Anime style, emotional dream world scene, young protagonist standing in a warm traditional blacksmith forge with his family, tears in his eyes as he draws his black katana to break the illusion, dramatic lighting"),
    ("escena_c5_e3.jpg", "Anime style, epic dark fantasy climax, vintage train car transforming into organic demon flesh and teeth, young swordsman unleashing a flaming sword strike on the roof, pale demon standing atop the train under the full moon, masterpiece manga artwork")
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
    v2_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-2"
    print("=== RENDERING VOL 2 LOCAL IMAGES ===")
    render_batch(VOL2_PROMPTS, v2_dir)
    print("=== VOL 2 LOCAL IMAGES GENERATED SUCCESSFULLY ON RTX 3060! ===")
