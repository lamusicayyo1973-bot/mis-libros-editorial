import os
import sys
import shutil
import urllib.request
import json
from gradio_client import Client

client = Client("http://127.0.0.1:7865/")

PROMPTS = [
    {
        "filename": "escena_c2_e2.jpg",
        "prompt": "Anime style, epic dual finisher strike, two young swordsmen unleashing a combined attack of red flames and yellow lightning into the dark glowing core of a train boiler, massive energy explosion, G-pen style"
    },
    {
        "filename": "escena_c2_e3.jpg",
        "prompt": "Anime style, dark fantasy crash aftermath, overturned vintage train on a grassy field at dawn, glowing red embers rising, young protagonist standing exhausted beside a sleeping companion in a yellow haori, dramatic atmospheric shot"
    },
    {
        "filename": "escena_c3_e1.jpg",
        "prompt": "Anime style, terrifying villain appearance, pale martial artist demon with blue tattoos on his pale skin and glowing golden eyes with lunar marks, walking out of a dark forest at dawn, crushing aura pressure, high tension, detailed art"
    },
    {
        "filename": "escena_c3_e2.jpg",
        "prompt": "Anime style, dramatic confrontation, powerful flame swordsman holding a glowing orange katana facing a tattooed martial artist demon in a fighting stance, grassy field background at sunrise, high contrast lighting"
    },
    {
        "filename": "escena_c3_e3.jpg",
        "prompt": "Anime style, high-speed martial arts vs sword action, flame swordsman unleashing a giant golden fire tiger attack against a tattooed demon throwing energy punches, explosion of dust and fire, dynamic camera angle"
    },
    {
        "filename": "escena_c4_e1.jpg",
        "prompt": "Anime style, dramatic battle moment, injured swordsman with blood on his face smiling heroically while enveloping his katana in blinding white fire, tattooed demon watching in respect, emotional intensity, G-pen line art"
    },
    {
        "filename": "escena_c4_e2.jpg",
        "prompt": "Anime style, epic dramatic climax, swordsman pinning a tattooed demon by the neck with a glowing white flaming sword while the demon's fist is embedded in his torso, sunrise light appearing on the horizon, masterpiece artwork"
    },
    {
        "filename": "escena_c4_e3.jpg",
        "prompt": "Anime style, emotional anger scene, young protagonist crying and shouting toward a dark forest as a tattooed demon flees into the shadows, a black katana embedded in the demon's back, morning sunlight background"
    },
    {
        "filename": "escena_c5_e1.jpg",
        "prompt": "Anime style, emotional farewell scene, dying flame swordsman sitting peacefully under the morning sun resting his hand on the head of a crying young protagonist, demon sister watching sadly, warm golden lighting"
    },
    {
        "filename": "escena_c5_e2.jpg",
        "prompt": "Anime style, spiritual farewell moment, spirit of a mother in a kimono appearing in golden light to embrace a smiling swordsman, peaceful closure, artistic lighting, detailed character design"
    },
    {
        "filename": "escena_c5_e3.jpg",
        "prompt": "Anime style, heroic determination scene, young protagonist with a flame-shaped mark on his face walking down a path carrying a flame sword guard on his black katana, sunny blue sky, epic journey continuation, masterpiece manga art"
    }
]

def generate_local(prompt_text):
    req_data = {
        "data": [
            True, prompt_text, "low quality, blurry, worst quality, deformed",
            ["Fooocus V2", "Fooocus Masterpiece"], "Speed", "1152×648", 1, "png", 42,
            False, 2.0, 7.0, "juggernautXL_v8Rundiffusion.safetensors", "None", 0.8,
            False, "None", 1.0, False, "None", 1.0, False, "None", 1.0, False, "None", 1.0, False, "None", 1.0,
            False, "image", "Disabled", None, [], None, "", None,
            False, False,
            False, None, False, None, False,
            "Disabled", "", "", "", "u2net", "full", "vit_b", 0.25, 0.3, 3, False, "None", 0.5, 0.0, 0, False,
            "Disabled", "", "", "", "u2net", "full", "vit_b", 0.25, 0.3, 3, False, "None", 0.5, 0.0, 0, False,
            "Disabled", "", "", "", "u2net", "full", "vit_b", 0.25, 0.3, 3, False, "None", 0.5, 0.0, 0, False
        ],
        "fn_index": 67
    }
    data = json.dumps(req_data).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:7865/run/predict", data=data, headers={'Content-Type': 'application/json'})
    
    try:
        response = urllib.request.urlopen(req)
        res = json.loads(response.read())
        return res
    except Exception as e:
        print("API call error:", e)
        return None

if __name__ == "__main__":
    out_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros\oni-no-ketsuryu-volumen-3"
    for item in PROMPTS:
        print(f"Generating local RTX 3060 scene: {item['filename']}...")
        generate_local(item["prompt"])
