# -*- coding: utf-8 -*-
"""
Selector de Carpetas Nativo de Windows para Loki (Thread-Safe Subprocess)
"""
import sys
import tkinter as tk
from tkinter import filedialog

def main():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder = filedialog.askdirectory(title="Seleccioná la carpeta de tu libro para Loki")
        root.destroy()
        if folder:
            print(folder.strip())
        else:
            print("CANCEL")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
