import sys
import io
import time
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from pathlib import Path
sys.path.insert(0, r"C:\pinokio\api\fooocus.git\app")

from gradio_client import Client

print("Connecting to Fooocus Gradio client at http://127.0.0.1:7860/...")
client = Client("http://127.0.0.1:7860/")

prompt = "Anime style, dark fantasy manga illustration, eight powerful swordsmen in ceremonial haoris gathered in a traditional Japanese hall illuminated by purple glowing wisteria flowers, frail leader sitting on a tatami mat, young protagonist with a flame mark standing resolute, G-pen ink style, highly detailed"

print("Submitting prompt to Fooocus...")
try:
    # Fooocus default generate endpoint is fn_index 68 or 73 or unnamed
    res = client.predict(
        False, # generate_image_grid
        prompt, # prompt
        "low quality, bad quality, blurry", # negative_prompt
        ["Fooocus V2", "Fooocus Masterpiece"], # style_selections
        "Speed", # performance_selection
        "1152×896", # aspect_ratios_selection
        1, # image_number
        "png", # output_format
        -1, # seed
        False, # read_wildcards_in_order
        2.0, # sharpness
        7.0, # cfg_scale
        "juggernautXL_v8Rundiffusion.safetensors", # base_model_name
        "None", # refiner_model_name
        0.8, # refiner_switch
        False, "None", 1.0, # lora 1
        False, "None", 1.0, # lora 2
        False, "None", 1.0, # lora 3
        False, "None", 1.0, # lora 4
        False, "None", 1.0, # lora 5
        False, # input_image_checkbox
        fn_index=32
    )
    print("Result:", res)
except Exception as e:
    print("Error calling Fooocus API:", e)
