from __future__ import annotations

import os
import socket
import sys
import threading
import time
import urllib.request
from pathlib import Path

import uvicorn
import webview

import server


class NativeAPI:
    """Native dialogs exposed to JavaScript through pywebview."""

    def __init__(self) -> None:
        self.window: webview.Window | None = None

    def select_file(self) -> list[str]:
        if self.window is None:
            return []
        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=True,
            file_types=("PDF files (*.pdf)",),
        )
        return list(result or [])

    def save_file(self, default_name: str = "merged.pdf", file_type: str = "PDF") -> str:
        if self.window is None:
            return ""

        if file_type.upper() == "DOCX":
            types = ("Word documents (*.docx)",)
        else:
            types = ("PDF files (*.pdf)",)

        result = self.window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename=default_name,
            file_types=types,
        )
        # pywebview returns a path string for SAVE_DIALOG.
        return str(result or "")


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_server(url: str, timeout: float = 15.0) -> None:
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=0.5) as response:
                if response.status == 200:
                    return
        except Exception as exc:
            last_error = exc
        time.sleep(0.05)
    raise RuntimeError(f"FastAPI did not start in time: {last_error}")


def run() -> None:
    port = find_free_port()
    config = uvicorn.Config(
        server.app,
        host="127.0.0.1",
        port=port,
        log_level="warning",
        access_log=False,
    )
    api_server = uvicorn.Server(config)

    thread = threading.Thread(target=api_server.run, daemon=True, name="uvicorn")
    thread.start()

    base_url = f"http://127.0.0.1:{port}"
    wait_for_server(f"{base_url}/health")

    native_api = NativeAPI()
    window = webview.create_window(
        "PDF Workbench",
        f"{base_url}/",
        js_api=native_api,
        width=1320,
        height=900,
        min_size=(960, 680),
        resizable=True,
        text_select=True,
    )
    native_api.window = window

    # pywebview chooses WebKit on macOS and WebView2 on Windows when the
    # corresponding native runtime is installed.
    webview.start(debug=False)

    api_server.should_exit = True
    thread.join(timeout=3)


if __name__ == "__main__":
    run()
