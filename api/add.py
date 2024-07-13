import ctypes
import ctypes.wintypes as wintypes

def add_keyboard_layout(layout_name):
    KLF_ACTIVATE = 1
    KLF_SUBSTITUTE_OK = 2

    ctypes.windll.user32.LoadKeyboardLayoutW.argtypes = [wintypes.LPCWSTR, wintypes.UINT]
    ctypes.windll.user32.LoadKeyboardLayoutW.restype = wintypes.HKL

    layout_handle = ctypes.windll.user32.LoadKeyboardLayoutW(layout_name, KLF_ACTIVATE | KLF_SUBSTITUTE_OK)

if __name__ == "__main__":
    layout_name = "0000040C"  # Layout ID for French (France)
    add_keyboard_layout(layout_name)
