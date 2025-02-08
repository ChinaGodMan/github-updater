import requests
import subprocess
import os
import re


def check_version():
    try:
        result = subprocess.run([f"{ChinaGodMan_U}\Program Files\command_line_tools\Clink\clink_x64.exe", "--version"], capture_output=True, text=True)
        ver = re.sub(r'\.[^.]*$', '', result.stdout.strip())
        return ver
    except subprocess.CalledProcessError as e:
        return None


def fetch_latest_release_url():
    url = "https://api.github.com/repos/chrisant996/clink/releases/latest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 解析返回的 JSON 数据
            data = response.json()
            # 获取 assets 列表中的第一个项目的 browser_download_url
            first_asset_url = data['assets'][0]['browser_download_url']
            return first_asset_url
        else:
            print(f"下载clink请求失败，状态码: {response.status_code}")
    except Exception as e:
        return (f"发生错误: {e}")


def unzip():
    print(f"开始解压{save_path}")
    command = f'7z x "{save_path}" -o"{unzip_folder}" -y'
    os.system(command)
