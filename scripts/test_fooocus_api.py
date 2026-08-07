import sys
import io
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from pathlib import Path
sys.path.insert(0, r"C:\pinokio\api\fooocus.git\app")

from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
print("Gradio Client connected successfully!")
info = client.view_api(return_format="dict")
print("Named endpoints:", list(info.get("named_endpoints", {}).keys()))
print("Unnamed endpoints:", list(info.get("unnamed_endpoints", {}).keys()))
