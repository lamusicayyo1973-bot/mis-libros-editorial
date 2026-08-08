# -*- coding: utf-8 -*-
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import diffusers
    print("diffusers version:", diffusers.__version__)
except ImportError:
    print("diffusers not installed directly, checking ldm_patched...")
    fooocus_dir = r"C:\pinokio\api\fooocus.git\app"
    sys.path.insert(0, fooocus_dir)
    import ldm_patched.modules.model_management as model_management
    print("ldm_patched available!")
