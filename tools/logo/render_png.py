"""Saves PNG copies of the logos (for Instagram, WhatsApp, printing).

Needs Google Chrome or Microsoft Edge installed.
Run:   python tools/logo/render_png.py            -> images/logo/png/
       python tools/logo/render_png.py OUT_DIR    -> somewhere else
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGOS = ROOT / "images" / "logo"
BROWSERS = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]
SCALE = 2   # 2 = double size, sharper PNGs


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else LOGOS / "png"
    out.mkdir(parents=True, exist_ok=True)
    browser = next((b for b in BROWSERS if b.exists()), None)
    if not browser:
        sys.exit("Chrome or Edge not found")

    for svg in sorted(LOGOS.glob("*.svg")):
        w, h = re.search(r'viewBox="0 0 (\S+) (\S+)"', svg.read_text(encoding="utf-8")).groups()
        png = out / (svg.stem + ".png")
        subprocess.run([str(browser), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--default-background-color=00000000", f"--force-device-scale-factor={SCALE}",
                        f"--window-size={w},{h}", f"--screenshot={png}", svg.as_uri()],
                       capture_output=True, timeout=60)
        print(("saved " if png.exists() else "FAILED ") + str(png))


if __name__ == "__main__":
    main()
