import requests
import requests as rq
import subprocess
import os


def CheckReleaseVersion():
    CHECKURL = 'https://github.com/zufuliu/notepad4/releases/latest'
    try:
        response = rq.get(CHECKURL, allow_redirects=False)
        if response.status_code == 302:
            version = response.headers["Location"].split("/")[-1]
            version = version.replace("v", "")
            version_parts = version.split("r")[0]
            return version_parts
        else:
            return "error"
    except Exception as e:
        return "error"


def check_version():
    ps_command = f'(Get-Item "{ChinaGodMan_U}\\Program Files\\notepad4\\Notepad4.exe").VersionInfo.FileVersion'
    result = subprocess.run(['pwsh', '-Command', ps_command], capture_output=True, text=True)
    if result.returncode == 0:
        version = result.stdout.strip()
        version_parts = version.split('.')
        if len(version_parts) >= 2:
            return '.'.join(version_parts[:2])
        else:
            return version
    else:
        print(f"错误: {result.stderr}")
        return None


def fetch_latest_release_url():
    url = "https://api.github.com/repos/zufuliu/notepad4/releases/latest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for asset in data['assets']:
                if "Notepad4_HD_zh-Hans_x64" in asset['name']:
                    return asset['browser_download_url']
            print("没有找到符合条件的下载链接")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except Exception as e:
        return f"发生错误: {e}"


def unzip():
    print(f"开始解压{save_path}")
    command = f'7z x "{save_path}" -o"{unzip_folder}" -y -xr!*.ini'
    os.system(command)
