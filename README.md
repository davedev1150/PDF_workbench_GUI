# PDF Workbench

A local, cross-platform PDF desktop utility built with:

- pywebview — native desktop window
- FastAPI + Uvicorn — localhost backend
- PyMuPDF — PDF rendering, page extraction and merging
- pdf2docx — PDF → Word
- PyInstaller — packaging

No cloud service is required.

## Development

Python 3.11 or 3.12 is recommended.

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python desktop.py
```

For the macOS native webview, pywebview uses Apple's WebKit backend.

### Windows

Install Python 3.11/3.12, then:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python desktop.py
```

For Windows, install the Microsoft Edge WebView2 Runtime if it is not already present. Modern Windows 10/11 installations normally have it.

## Features

- Multiple PDF import
- Native macOS/Windows file-open dialog inside pywebview
- Browser drag/drop fallback
- Page thumbnails rendered with PyMuPDF
- Drag-and-drop page reordering
- Remove individual pages
- Merge arbitrary selected/reordered pages
- PDF → DOCX conversion of the current page sequence
- Native save dialogs for PDF/DOCX
- Local temporary storage
- Automatic cleanup of old temporary files
- Localhost-only backend

## Packaging

Install PyInstaller:

```bash
pip install pyinstaller
```

Then:

```bash
python build.py
```

### macOS

Run the build on macOS:

```bash
python build.py
```

Output:

```text
dist/PDF Workbench.app
```

For a distributable macOS app, codesigning/notarization should be added for your developer certificate and Apple distribution workflow.

### Windows

Run the build on Windows:

```powershell
python build.py
```

Output:

```text
dist\PDF Workbench.exe
```

The executable is built for the architecture of the Python environment used to build it. Build a Windows executable on Windows and a macOS application on macOS; PyInstaller is not a cross-compiler.

## Important packaging note

`pdf2docx` depends on a larger Python/PDF stack than the basic merger. Test Word conversion on the target OS after packaging. If your PyInstaller version misses an indirect import, add the relevant hidden import to the build command/spec after observing the exact error.

## Security model

The backend binds to `127.0.0.1`, not `0.0.0.0`, so it is intended for the local machine only.

Native file selection passes the chosen local file path from pywebview to the localhost FastAPI process. Files are copied into an application-owned temporary directory before processing.

Do not expose this FastAPI server to a LAN/WAN without adding authentication, CSRF protection, strict CORS, path allowlisting and other server-side security controls.

## Project structure

```text
pdf_workbench/
├── desktop.py
├── server.py
├── index.html
├── requirements.txt
├── build.py
└── README.md
```
