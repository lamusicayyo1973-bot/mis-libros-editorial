import sys
import os
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

app_path = r"C:\pinokio\api\fooocus.git\app"
sys.path.insert(0, app_path)
os.chdir(app_path)

import modules.async_worker as async_worker
import modules.config as config
import modules.flags as flags
import args_manager

print("Initializing Fooocus async worker...")
# Let's inspect default args from webui
import webui

print("Fooocus webui loaded successfully!")
