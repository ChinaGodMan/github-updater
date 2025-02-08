import subprocess
import re
import os
import shutil


def check_version():
    scrcpy_path = fr"{ChinaGodMan_U}\Program Files\command_line_tools\scrcpy-win64-v2.5\scrcpy.exe"
    try:
        result = subprocess.run([scrcpy_path, "--version"], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            match = re.search(r"scrcpy (\d+\.\d+)", result.stdout.strip())
            if match:
                version = match.group(1)
                return version
            else:
                return None
        else:
            return None
    except FileNotFoundError:
        return None
    except Exception as e:
        return None


def clear_folder(folder_path):
    """
    清空指定文件夹下的所有内容，保留文件夹本身。

    :param folder_path: 要清空的文件夹路径
    """
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)  # 删除文件或符号链接


def unzip():
    print(f"开始解压{save_path}")
    command = f'7z x "{save_path}" -o"{unzip_folder}"  -y'
    os.system(command)
    src_folder = os.path.join(unzip_folder, f"scrcpy-win64-v{lasted_version}")
    clear_folder(unzip_folder)
    if os.path.exists(src_folder):
        for item in os.listdir(src_folder):
            shutil.move(os.path.join(src_folder, item), fr"{ChinaGodMan_U}\Program Files\command_line_tools\scrcpy-win64-v2.5")
    shutil.rmtree(src_folder)
    print(f"scrcpy更新完成")
