import os
import configparser
import requests
import requests as rq
import importlib.util
import tempfile
from tabulate import tabulate
# 动态获取
ChinaGodMan_U = os.getenv("ChinaGodMan_U", "C:")
temp_dir = tempfile.gettempdir()
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)


def download_file(url, output_path):
    """下载文件并显示进度"""
    try:
        with requests.get(url, stream=True) as response:
            if response.status_code != 200:
                print(f"下载失败，HTTP 状态码: {response.status_code}")
                return

            total_size = int(response.headers.get('Content-Length', 0))
            with open(output_path, 'wb') as file:
                downloaded_size = 0
                chunk_size = 1048576
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            percent_complete = (
                                downloaded_size / total_size) * 100
                            print(
                                f"\r下载中: {percent_complete:.2f}% 已完成", end='')

        print(f"\n文件已成功下载到: {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")


def load_ini(file_path):
    """加载 ini 配置文件"""
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")
    return config


def execute_plugin(plugin_path, function_name, env):
    """动态加载插件并执行函数"""
    try:
        spec = importlib.util.spec_from_file_location(
            "plugin_module", plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for i in range(0, len(env), 2):
            key = env[i]
            value = env[i + 1]
            setattr(module, key, value)
        if hasattr(module, function_name):
            func = getattr(module, function_name)
            return func()
        else:
            print(f"函数 {function_name} 不存在于 {plugin_path} 中")
            return None
    except Exception as e:
        print(f"执行插件时出错: {e}")
        return None


def CheckReleaseVersion(CHECKURL):
    try:
        response = rq.get(CHECKURL,
                          allow_redirects=False)
        if response.status_code == 302:
            version = response.headers["Location"].split("/")[-1]
            version = version.replace("v", "")
            return version
        else:
            return "error"
    except:
        return "error"


def process_section(section_name, config):
    """处理配置节内容"""
    description = config.get(section_name, "description")
    release_url = config.get(section_name, "release_url")
    download_url = config.get(section_name, "download_url")
    unzip_folder = config.get(section_name, "unzip_folder").format(
        ChinaGodMan_U=ChinaGodMan_U)
    save_path = config.get(section_name, "save_path")
    plugin = os.path.join(current_dir, "utils", config.get(section_name, "plugin"))
    print(f" {plugin}")
    check_version = config.get(section_name, "check_version")
    done = config.get(section_name, "done")

    # 检查最新版本
    latest_version = CheckReleaseVersion(release_url)
    env = ["save_path", save_path, "version", "1.2.3"]
    print(f"{section_name} 最新版本: {latest_version}")
    if latest_version is None:
        latest_version = execute_plugin(plugin, check_version, env)

    # 检查本地版本
    local_version = execute_plugin(plugin, check_version, env)
    print(f"{section_name} 本地版本: {local_version}")
    if local_version is None:
        print(f"{section_name} 本地版本检查失败")
        return

    save_path = save_path.format(
        temp_dir=temp_dir, lasted_version=latest_version, ChinaGodMan_U=ChinaGodMan_U)
    if latest_version != local_version:
        print(f"发现新版本，正在更新 {section_name}")
        download_url = download_url.format(lasted_version=latest_version)
        print(f"下载地址: {download_url}, 保存路径: {save_path}")
        download_file(download_url, save_path)
        env = ["save_path", save_path, "lasted_version", latest_version, "ChinaGodMan_U", ChinaGodMan_U, "unzip_folder", unzip_folder]
        execute_plugin(plugin, done, env)
    else:
        print(f"{section_name} 已是最新版本，无需更新。")


ini_file_path = fr"{current_dir}\softs.ini"
config = load_ini(ini_file_path)
print("GitHub软件更新程序")
menu = []
for index, section in enumerate(config.sections(), start=1):
    description = config.get(section, "description")
    menu.append([str(index), section, description])

menu.append(["0", "退出", "退出程序"])
# 居中
colalign = ("center", "center", "center")
print(tabulate(menu, headers=["序号", "名称", "功能"],
      tablefmt="fancy_grid", colalign=colalign))

while True:
    choice = input("请输入数字选择功能 (输入 0 退出程序)：")
    if choice == "0":
        print("退出程序。")
        break
    elif choice.isdigit() and 1 <= int(choice) <= len(config.sections()):
        section_name = config.sections()[int(choice) - 1]
        process_section(section_name, config)
    else:
        print("无效选择，请重新输入。")
