# -*- coding: utf-8 -*-
import sys
import io
import os
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set working directory to fooocus app
fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

import modules.async_worker as worker
import modules.flags as flags
import modules.config as config

print("Fooocus async_worker loaded successfully!")

# Let's inspect worker.generate_click signature
import inspect
sig = inspect.signature(worker.generate_click)
print("generate_click parameters count:", len(sig.parameters))
