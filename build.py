"""
PyInstaller helper.

Usage:
    python build.py

Or directly:
    pyinstaller --clean --noconfirm PDFWorkBench.spec

The generated artifact is platform-specific:
  macOS  -> dist/PDF Workbench.app
  Windows -> dist/PDF Workbench.exe
"""
from pathlib import Path
import PyInstaller.__main__

ROOT = Path(__file__).resolve().parent

args = [
    str(ROOT / "desktop.py"),
    "--name=PDF Workbench",
    "--clean",
    "--noconfirm",
    "--windowed",
    "--onefile",
    "--add-data=index.html:.",
]

# PyInstaller uses ';' as the add-data separator on Windows and ':' elsewhere.
if __import__("sys").platform.startswith("win"):
    args[-1] = "--add-data=index.html;."

PyInstaller.__main__.run(args)
