# -*- coding: utf-8 -*-
import sys
import io
import asyncio
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Testing Playwright / Selenium availability...")

try:
    from playwright.async_api import async_playwright
    print("Playwright is installed!")
except ImportError:
    print("Playwright is NOT installed in current Python env.")

try:
    import selenium
    print("Selenium is installed!")
except ImportError:
    print("Selenium is NOT installed in current Python env.")
