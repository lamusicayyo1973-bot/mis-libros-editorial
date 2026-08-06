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

VOL3_PROMPTS = [
    ("escena_c1_e1.jpg", "Anime style, dark fantasy action scene, flame-patterned haori swordsman unleashing a wave of golden fire inside a train car covered in organic demon flesh, young black-haired protagonist dodging tentacles, high intensity, G-pen manga art"),
    ("escena_c1_e2.jpg", "Anime style, dynamic tag-team action, young swordsman unleashing red flaming sword strikes alongside his demon sister with a bamboo gag using purple flames to protect sleeping train passengers, dark organic train interior, epic artwork"),
    ("escena_c1_e3.jpg", "Anime style, character transformation scene, young swordsman in a yellow lightning-patterned haori sleeping standing up on a train roof under the moon, electricity sparking around his dual short katanas, dramatic low angle, G-pen line art"),
    ("escena_c2_e1.jpg", "Anime style, lightning fast sword strike, sleeping swordsman in yellow haori leaving a yellow lightning trail cutting through demon tentacles on a train roof, protagonist leaping toward a glowing dark core inside the engine, epic manga art"),
    ("escena_c2_e2.jpg", "Anime style, epic dual finisher strike, two young swordsmen unleashing a combined attack of red flames and yellow lightning into the dark glowing core of a train boiler, massive energy explosion, G-pen style"),
    ("escena_c2_e3.jpg", "Anime style, dark fantasy crash aftermath, overturned vintage train on a grassy field at dawn, glowing red embers rising, young protagonist standing exhausted beside a sleeping companion in a yellow haori, dramatic atmospheric shot"),
    ("escena_c3_e1.jpg", "Anime style, terrifying villain appearance, pale martial artist demon with blue tattoos on his pale skin and glowing golden eyes with lunar marks, walking out of a dark forest at dawn, crushing aura pressure, high tension, detailed art"),
    ("escena_c3_e2.jpg", "Anime style, dramatic confrontation, powerful flame swordsman holding a glowing orange katana facing a tattooed martial artist demon in a fighting stance, grassy field background at sunrise, high contrast lighting"),
    ("escena_c3_e3.jpg", "Anime style, high-speed martial arts vs sword action, flame swordsman unleashing a giant golden fire tiger attack against a tattooed demon throwing energy punches, explosion of dust and fire, dynamic camera angle"),
    ("escena_c4_e1.jpg", "Anime style, dramatic battle moment, injured swordsman with blood on his face smiling heroically while enveloping his katana in blinding white fire, tattooed demon watching in respect, emotional intensity, G-pen line art"),
    ("escena_c4_e2.jpg", "Anime style, epic dramatic climax, swordsman pinning a tattooed demon by the neck with a glowing white flaming sword while the demon's fist is embedded in his torso, sunrise light appearing on the horizon, masterpiece artwork"),
    ("escena_c4_e3.jpg", "Anime style, emotional anger scene, young protagonist crying and shouting toward a dark forest as a tattooed demon flees into the shadows, a black katana embedded in the demon's back, morning sunlight background"),
    ("escena_c5_e1.jpg", "Anime style, emotional farewell scene, dying flame swordsman sitting peacefully under the morning sun resting his hand on the head of a crying young protagonist, demon sister watching sadly, warm golden lighting"),
    ("escena_c5_e2.jpg", "Anime style, spiritual farewell moment, spirit of a mother in a kimono appearing in golden light to embrace a smiling swordsman, peaceful closure, artistic lighting, detailed character design"),
    ("escena_c5_e3.jpg", "Anime style, heroic determination scene, young protagonist with a flame-shaped mark on his face walking down a path carrying a flame sword guard on his black katana, sunny blue sky, epic journey continuation, masterpiece manga art")
]

VOL4_PROMPTS = [
    ("escena_c1_e1.jpg", "Anime style, dark fantasy manga illustration, old retired swordsman presenting an ancient scroll book to a young black-haired protagonist with a flame-shaped face mark, traditional Japanese room with sliding doors at dusk, G-pen ink style, highly detailed"),
    ("escena_c1_e2.jpg", "Anime style, swordsman practicing a traditional ritual dance with a katana emitting radiant golden fire, traditional Japanese dojo background, glowing embers floating in the air, dynamic motion blur, high quality manga art"),
    ("escena_c1_e3.jpg", "Anime style, dialogue scene, young swordsman with a flame mark talking to a quiet girl in a white kimono with a fox mask and purple butterfly accessories, traditional Japanese garden at sunset, scenic artwork"),
    ("escena_c2_e1.jpg", "Anime style, dark fantasy environment, glowing traditional Japanese entertainment district at night with red silk lanterns, three undercover protagonists in kimonos walking across a wooden bridge, atmospheric lighting, detailed background art"),
    ("escena_c2_e2.jpg", "Anime style, villain reveal scene, beautiful woman in an elaborate kimono with glowing green marks on her eyes, a giant glowing silk obi sash floating around her like sharp blades inside a traditional Japanese room, dark fantasy aesthetic"),
    ("escena_c2_e3.jpg", "Anime style, dynamic combat inside a collapsing wooden house, young swordsman deflecting razor-sharp silk sashes with a glowing sword, anime girl with bamboo gag leaping into battle, floating silk sashes, high action energy"),
    ("escena_c3_e1.jpg", "Anime style, moonlight rooftop battle, young swordsman delivering a golden fire strike decapitating a demon woman in an elaborate kimono, purple flames burning in the background, dramatic composition, G-pen line art"),
    ("escena_c3_e2.jpg", "Anime style, terrifying dual boss reveal, skeletal green-skinned demon holding two bone sickles emerging from the back of a decapitated demon woman, explosive blast of red poisonous arcs, high destruction scale"),
    ("escena_c3_e3.jpg", "Anime style, desperate battle scene, young protagonist on his knees on a rooftop with black poison veins spreading on his neck, skeletal demon standing over him with a bone sickle, moonlight sky, high tension"),
    ("escena_c4_e1.jpg", "Anime style, healing and support scene, anime girl with bamboo gag using purple flames to burn away green poison from her brother's shoulder, brother standing up with glowing eyes, dynamic team battle, detailed artwork"),
    ("escena_c4_e2.jpg", "Anime style, epic sun dance technique, young swordsman transformed into a phoenix of golden fire charging at a skeletal demon, simultaneous lightning strike in the background rooftop, masterpiece manga artwork"),
    ("escena_c4_e3.jpg", "Anime style, double decapitation victory, simultaneous golden fire and yellow lightning strikes severing the heads of two demon siblings, massive explosion of light and embers over a Japanese city, epic scale"),
    ("escena_c5_e1.jpg", "Anime style, emotional afterlife scene, human child spirits of two demon siblings crying in a dark misty alley, young protagonist kneeling beside them with a gentle expression, quiet melancholy mood"),
    ("escena_c5_e2.jpg", "Anime style, emotional redemption moment, human spirit of a brother carrying his little sister on his back walking into gentle golden flames, young protagonist and his demon sister watching hand in hand, detailed art"),
    ("escena_c5_e3.jpg", "Anime style, terrifying villain assembly, elegant demon king with crimson cat eyes standing furiously in an infinite floating Japanese castle with gravity-defying architecture, four powerful demon lords kneeling before him, masterpiece manga artwork")
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
    v3_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-3"
    v4_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-4"
    
    print("=== RENDERING VOL 3 LOCAL IMAGES ===")
    render_batch(VOL3_PROMPTS, v3_dir)
    
    print("=== RENDERING VOL 4 LOCAL IMAGES ===")
    render_batch(VOL4_PROMPTS, v4_dir)
    
    print("=== ALL LOCAL IMAGES GENERATED SUCCESSFULLY ON RTX 3060! ===")
