import subprocess
import os


def get_powershell_version():
    """
    获取 PowerShell 版本号。

    返回:
        str: PowerShell 版本号，如果获取失败则返回 None。
    """
    ps_command = "$PSVersionTable.PSVersion.ToString()"
    try:
        result = subprocess.run(
            ["pwsh", "-Command", ps_command], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("执行 PowerShell 命令时出错:", e.stderr)
        return None


def unzip():
    print(f"开始解压{save_path}")
    command = f'7z x "{save_path}" -o"{unzip_folder}" -y'
    os.system(command)
