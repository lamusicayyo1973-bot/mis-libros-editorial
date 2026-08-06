import urllib.request
import json

req_data = {
    "data": [
        True, # generate_image_grid
        "Anime style, dark fantasy manga illustration, young swordsman desheathing a jet-black katana with a glowing thin red line along the edge", # prompt
        "low quality, blurry", # negative_prompt
        ["Fooocus V2"], # style_selections
        "Speed", # performance_selection
        "1152×648", # aspect_ratios_selection
        1, # image_number
        "png", # output_format
        12345, # seed
        False, 2.0, 7.0,
        "juggernautXL_v8Rundiffusion.safetensors",
        "None", 0.8,
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
    print("Fooocus HTTP generation triggered! Response keys:", list(res.keys()))
    if "data" in res:
        print("Data response received:", res["data"])
except Exception as e:
    print("Error calling Fooocus HTTP endpoint:", e)
