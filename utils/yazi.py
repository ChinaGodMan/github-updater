import requests
import subprocess
import os
import re


def check_version():
    try:
        yazi_path = r"ya"
        result = subprocess.run([yazi_path, "--version"], capture_output=True, text=True, check=True)
        match = re.search(r"Ya\s+([\d.]+)", result.stdout.strip())
        if match:
            return match.group(1)
        else:
            return None
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None
    except Exception as e:
        return None


def unzip():
    print(f"开始解压{save_path}")
    command = f'7z x "{save_path}" -o"{unzip_folder}" -y'
    os.system(command)
