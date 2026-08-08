import os
import sys
import shutil
from gradio_client import Client

client = Client("http://127.0.0.1:7865/")

PROMPTS = [
    {
        "book": "oni-no-ketsuryu-volumen-2",
        "filename": "escena_1.jpg",
        "prompt": "Anime style, dark fantasy manga illustration, young swordsman desheathing a jet-black katana with a glowing thin red line along the edge, eccentric blacksmith wearing a Hyottoko mask standing nearby, atmospheric lighting, G-pen line art"
    },
    {
        "book": "oni-no-ketsuryu-volumen-2",
        "filename": "escena_climax.jpg",
        "prompt": "Anime style, dramatic dark fantasy combat, young swordsman unleashing a flaming crescent slash from twin short katanas against a giant shadow demon on a snow peak, vivid purple wisteria glowing in background"
    },
    {
        "book": "oni-no-ketsuryu-volumen-3",
        "filename": "escena_1.jpg",
        "prompt": "Anime style, dark fantasy scene inside a demon train carriage, fleshy demonic tendrils writhing on seats, fiery golden aura surrounding a Flame Sables de Elite warrior with a flame haori desheathing bright orange katana"
    },
    {
        "book": "oni-no-ketsuryu-volumen-3",
        "filename": "escena_climax.jpg",
        "prompt": "Anime style, epic nighttime battle on top of a moving steam train engine, young warrior unleashing a sun-breathing fiery slash at a giant demonic engine face in a dark forest, sparks flying"
    },
    {
        "book": "oni-no-ketsuryu-volumen-4",
        "filename": "escena_1.jpg",
        "prompt": "Anime style, dark fantasy courtyard at sunset, ancient retired Flame Sables de Elite dropping a sake cup in shock seeing a black katana with a flame guard and crimson Sun Mark on young warrior's cheek"
    },
    {
        "book": "oni-no-ketsuryu-volumen-4",
        "filename": "escena_climax.jpg",
        "prompt": "Anime style, mirror district battle at night, dual demon siblings fighting young warrior and butterfly Sables de Elite, glowing purple poison butterflies swirling, high contrast dark fantasy art"
    }
]

def process_all():
    base_dir = r"c:\Users\nicol\Downloads\MIS LIBROS\libros"
    
    for item in PROMPTS:
        target_path = os.path.join(base_dir, item["book"], item["filename"])
        print(f"Generating local image for {item['book']}/{item['filename']} on RTX 3060...")
        
        try:
            # Call Fooocus predict API fn_index 67 (Generate)
            res = client.predict(
                True, # generate_image_grid
                item["prompt"], # prompt
                "low quality, blurry, deformed, text watermark", # negative_prompt
                ["Fooocus V2", "Fooocus Masterpiece"], # style_selections
                "Speed", # performance_selection
                "1152×648", # aspect_ratios_selection
                1, # image_number
                "png", # output_format
                12345, # seed
                False, # read_wildcards_in_order
                2.0, # sharpness
                7.0, # cfg_scale
                "juggernautXL_v8Rundiffusion.safetensors", # base_model_name
                "None", # refiner_model_name
                0.8, # refiner_switch
                False, "None", 1.0, False, "None", 1.0, False, "None", 1.0, False, "None", 1.0, False, "None", 1.0,
                False, "image", "Disabled", None, [], None, "", None,
                False, False,
                False, None, False, None, False,
                "Disabled", "", "", "", "u2net", "full", "vit_b", 0.25, 0.3, 3, False, "None", 0.5, 0.0, 0, False,
                "Disabled", "", "", "", "u2net", "full", "vit_b", 0.25, 0.3, 3, False, "None", 0.5, 0.0, 0, False,
                "Disabled", "", "", "", "u2net", "full", "vit_b", 0.25, 0.3, 3, False, "None", 0.5, 0.0, 0, False,
                fn_index=67
            )
            
            # Extract generated image path from Gradio response
            if res and len(res) > 3 and res[3]:
                gallery = res[3]
                if isinstance(gallery, list) and len(gallery) > 0:
                    img_info = gallery[0]
                    src_file = img_info.get("name") if isinstance(img_info, dict) else img_info
                    if src_file and os.path.exists(src_file):
                        shutil.copy(src_file, target_path)
                        print(f"✅ Generated & Saved to {target_path}")
        except Exception as e:
            print(f"Error generating {item['filename']}:", e)

if __name__ == "__main__":
    process_all()
