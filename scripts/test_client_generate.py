# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from gradio_client import Client
import time
from pathlib import Path
import shutil

print("Connecting to Fooocus Gradio client...")
client = Client("http://127.0.0.1:7860/", verbose=False)

prompt_text = "Anime style, dark fantasy manga illustration, young protagonist with a flame face mark, holding a glowing red katana in a dark cave, masterpiece artwork --ar 16:9"

print(f"Submitting prompt: {prompt_text}")
# Submit job to predict API endpoint 33 or named generate endpoint
try:
    res = client.predict(
        prompt_text, # prompt
        "", # negative prompt
        ["Fooocus V2", "Fooocus Masterpiece"], # styles
        "Speed", # performance
        "1152×896", # aspect ratio
        1, # image number
        "png", # output format
        "12345", # seed
        0.5, # sharpness
        "juggernautXL_v8Rundiffusion.safetensors", # base model
        "None", # refiner
        0.5, # refiner switch
        api_name="/generate"
    )
    print("Generation result:", res)
except Exception as e:
    print("Error calling /generate:", e)
