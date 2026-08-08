# -*- coding: utf-8 -*-
import sys
import io
import os
import ctypes
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src_path = r"C:\Users\nicol\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"
dest_path = r"C:\Proyectos\mis-libros-editorial\scratch\Cookies.db"

# Windows API constants
GENERIC_READ = 0x80000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_DELETE = 0x00000004
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x80

kernel32 = ctypes.windll.kernel32

handle = kernel32.CreateFileW(
    src_path,
    GENERIC_READ,
    FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
    None,
    OPEN_EXISTING,
    FILE_ATTRIBUTE_NORMAL,
    None
)

if handle == -1 or handle == 0xFFFFFFFF:
    print("Error abriendo archivo con CreateFileW:", kernel32.GetLastError())
else:
    print("Handle abierto exitosamente con Win32 API!")
    file_size = kernel32.GetFileSize(handle, None)
    buffer = ctypes.create_string_buffer(file_size)
    bytes_read = ctypes.c_ulong(0)
    
    if kernel32.ReadFile(handle, buffer, file_size, ctypes.byref(bytes_read), None):
        with open(dest_path, "wb") as f:
            f.write(buffer.raw[:bytes_read.value])
        print(f"¡Base de datos Cookies copiada ({bytes_read.value} bytes) exitosamente!")
    else:
        print("Error leyendo datos del handle:", kernel32.GetLastError())
        
    kernel32.CloseHandle(handle)
