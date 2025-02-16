import re
import subprocess


def get_code_version():
    try:
        result = subprocess.run("code --version | head -n 1", shell=True, stdout=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "未找到 `code` 命令，请确保 Visual Studio Code 已安装并添加到 PATH。"
    except subprocess.CalledProcessError as e:
        return f"执行命令时出错：{e}"
    except Exception as e:
        return f"发生未知错误：{e}"


def replace_text_in_file(file_path, pattern, replacement):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        updated_content = re.sub(pattern, replacement, content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"替换完成：{file_path}")
    except Exception as e:
        print(f"发生错误：{e}")


def update_version():
    file_path = fr"{ChinaGodMan_U}\GitHub\disk\PortableInstall\ConfigFiles\portable-app-config.json"
    print(file_path)
    pattern = r"(?<=/ZIP/VSCode/VSCode-win32-x64-).*?(?=\.zip)"
    replace_text_in_file(file_path, pattern, latest_version)
