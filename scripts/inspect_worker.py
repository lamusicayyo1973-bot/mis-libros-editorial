# -*- coding: utf-8 -*-
import sys
import io
import os
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

fooocus_dir = Path(r"C:\pinokio\api\fooocus.git\app")
os.chdir(str(fooocus_dir))
sys.path.insert(0, str(fooocus_dir))

import modules.async_worker as worker

print("Worker attributes:", [a for a in dir(worker) if not a.startswith("_")])
