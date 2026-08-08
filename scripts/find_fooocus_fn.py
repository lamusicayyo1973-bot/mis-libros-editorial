# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from gradio_client import Client

client = Client("http://127.0.0.1:7860/", verbose=False)
for fn_index, info in enumerate(client.endpoints):
    inputs = [getattr(param, "label", str(param)) for param in getattr(info, "parameters", [])]
    print(f"fn_index={fn_index}: {inputs[:3]}")
