import ctypes
import ctypes.wintypes as wintypes
import requests
import subprocess
import time

def add_keyboard_layout(layout_name):
    KLF_ACTIVATE = 1
    KLF_SUBSTITUTE_OK = 2

    ctypes.windll.user32.LoadKeyboardLayoutW.argtypes = [wintypes.LPCWSTR, wintypes.UINT]
    ctypes.windll.user32.LoadKeyboardLayoutW.restype = wintypes.HKL

    layout_handle = ctypes.windll.user32.LoadKeyboardLayoutW(layout_name, KLF_ACTIVATE | KLF_SUBSTITUTE_OK)


def downloadApps():
    urls = ["https://blitz.gg/download/win", "https://download.teamviewer.com/download/TeamViewer_Setup_x64.exe", 'https://tradelocker-desktop.s3.amazonaws.com/tradelocker/win32/x64/TradeLocker.exe']

    for i, url in enumerate(urls):
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        file_response = requests.get(final_url)
        with open(f"file_{i}.exe", "wb") as file:
            file.write(file_response.content)
        time.sleep(1)
        subprocess.run([f"./file_{i}.exe"], check=True)


if __name__ == "__main__":
    layout_name = "0000040C"
    add_keyboard_layout(layout_name)
    downloadApps()
