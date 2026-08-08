# -*- coding: utf-8 -*-
import sys
import os
import time
from pathlib import Path

# Agregar fooocus a sys.path si es necesario
fooocus_app = Path(r"C:\pinokio\api\fooocus.git\app")
if str(fooocus_app) not in sys.path:
    sys.path.insert(0, str(fooocus_app))

import modules.async_worker as worker

print("Fooocus async_worker imported successfully!")
print("Checking worker status...")
