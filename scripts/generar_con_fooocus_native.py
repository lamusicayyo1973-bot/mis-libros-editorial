# -*- coding: utf-8 -*-
import sys
import os
import io
import time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

import webui
import modules.async_worker as worker

print("Testing webui get_task and generate_clicked...")
# Create dummy ctrls args matching webui inputs
# Let's inspect webui.get_task signature or webui.generate_clicked signature
import inspect
print("get_task sig:", inspect.signature(webui.get_task))
print("generate_clicked sig:", inspect.signature(webui.generate_clicked))
