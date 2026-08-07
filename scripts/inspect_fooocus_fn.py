import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
api_info = client.view_api(return_format="dict")

for i, fn in enumerate(api_info.get("unnamed_endpoints", [])):
    print(f"fn_index={i}: inputs={len(fn.get('parameters', []))}, outputs={len(fn.get('returns', []))}")
