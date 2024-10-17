import ctypes
import ctypes.wintypes as wintypes
import requests
import subprocess
import time
import os
import urllib.request


def add_keyboard_layout(layout_name):
    KLF_ACTIVATE = 1
    KLF_SUBSTITUTE_OK = 2

    ctypes.windll.user32.LoadKeyboardLayoutW.argtypes = [
        wintypes.LPCWSTR, wintypes.UINT]
    ctypes.windll.user32.LoadKeyboardLayoutW.restype = wintypes.HKL

    layout_handle = ctypes.windll.user32.LoadKeyboardLayoutW(
        layout_name, KLF_ACTIVATE | KLF_SUBSTITUTE_OK)


def downloadApps():
    urls = ["https://blitz.gg/download/win",
            "https://download.teamviewer.com/download/TeamViewer_Setup_x64.exe"]

    for i, url in enumerate(urls):
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        file_response = requests.get(final_url)
        with open(f"file_{i}.exe", "wb") as file:
            file.write(file_response.content)
        time.sleep(1)
        subprocess.run([f"./file_{i}.exe"], check=True)


def clone_and_install_projects():
    projects = [
        {
            'repo': 'https://github.com/mrhan1993/Fooocus-API',
            'install_cmd': 'python -m pip install venv && python -m venv venv && .\\venv\\Scripts\\activate && pip install -r requirements.txt && pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu126'
        },
    ]

    base_dir = os.path.join(os.getcwd(), "cloned_projects")
    os.makedirs(base_dir, exist_ok=True)

    for project in projects:
        repo_url = project['repo']
        install_cmd = project['install_cmd']

        repo_name = os.path.basename(repo_url).replace('.git', '')
        project_dir = os.path.join(base_dir, repo_name)

        subprocess.run(['git', 'clone', repo_url, project_dir], check=True)

        os.chdir(project_dir)

        subprocess.run(install_cmd, shell=True, check=True)

        os.chdir(base_dir)


def download_and_install_apps():
    # URLs for each application's installer
    apps = {
        "git": {
            "url": "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.1/Git-2.42.0-64-bit.exe",
            "installer_name": "git_installer.exe",
            "install_args": ['/SILENT', '/NORESTART']
        },
        "cuda": {
            "url": "https://developer.download.nvidia.com/compute/cuda/12.6.2/local_installers/cuda_12.6.2_560.94_windows.exe",
            "installer_name": "cuda_installer.exe",
            "install_args": ['-s', '-noreboot']
        },
        "python": {
            "url": "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe",
            "installer_name": "python_installer.exe",
            "install_args": ['/quiet', 'InstallAllUsers=1', 'PrependPath=1']
        }
    }

    # Function to download and install each app
    def download_and_install(app_name, app_info):
        installer_path = os.path.join(os.getcwd(), app_info["installer_name"])

        # Download the installer
        print(f"Downloading {app_name} installer...")
        urllib.request.urlretrieve(app_info["url"], installer_path)

        # Run the installer with silent options
        print(f"Installing {app_name}...")
        subprocess.run([installer_path] + app_info["install_args"], check=True)

        # Clean up installer file
        os.remove(installer_path)
        print(f"{app_name.capitalize()} installed successfully.")

    # Download and install Git, CUDA, and Python
    for app_name, app_info in apps.items():
        download_and_install(app_name, app_info)


if __name__ == "__main__":
    layout_name = "0000040C"
    add_keyboard_layout(layout_name)
    download_and_install_apps()
    downloadApps()
