# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from gradio_client import Client
import json

client = Client("http://127.0.0.1:7860/")
print("Gradio Client connected successfully!")
api_info = client.view_api(return_format="dict")
print("API Endpoints:")
for fn_index, details in api_info.get("named_endpoints", {}).items():
    print(f"Endpoint {fn_index}: {details}")
