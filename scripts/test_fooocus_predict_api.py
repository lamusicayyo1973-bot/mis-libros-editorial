# -*- coding: utf-8 -*-
import urllib.request
import json
import time
from pathlib import Path

url = "http://127.0.0.1:7860/run/predict"

# Construct payload matching Fooocus gradio interface
payload = {
    "fn_index": 33, # or primary generate handler index
    "data": [
        "Anime style, dark fantasy manga illustration, young protagonist with flame face mark holding glowing red katana in a hot spring village", # prompt
        "", # negative prompt
        ["Fooocus V2", "Fooocus Masterpiece"], # styles
        "Speed", # performance
        "1152×896", # aspect ratio
        1, # image_number
        "png", # output_format
        "12345", # seed
        False, # read_wildcards
        0.5, # sharpness
        4.0, # guidance_scale
        "juggernautXL_v8Rundiffusion.safetensors", # base_model
        "None", # refiner_model
        0.5, # refiner_switch
    ]
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        res_text = response.read().decode('utf-8')
        print("Response status:", response.status)
        print("Response body:", res_text[:300])
except Exception as e:
    print("API Error:", e)
