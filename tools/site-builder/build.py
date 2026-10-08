"""Builds every page of the site.

Run from the project folder:   python tools/site-builder/build.py
"""
from pathlib import Path

import page_contact
import page_home
import page_shop

ROOT = Path(__file__).resolve().parents[2]

PAGES = {
    "index.html": page_home.build,
    "shop.html": page_shop.build,
    "contact.html": page_contact.build,
}

for name, build in PAGES.items():
    (ROOT / name).write_text(build(), encoding="utf-8")
    print("wrote", name)
