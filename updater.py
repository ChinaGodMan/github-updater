import os
import configparser
import requests
import requests as rq
import importlib.util
import tempfile
import json
import inspect
import locale
from tabulate import tabulate


os.system('mode con: cols=150 lines=30')


def get_country():
    locale_info = locale.getdefaultlocale()
    if locale_info and locale_info[0]:
        return locale_info[0]
    return None


def load_messages(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


def translate(key, **kwargs):
    message = messages.get(key, f"[{key}]")
    caller_locals = inspect.currentframe().f_back.f_locals
    context = {**caller_locals, **kwargs}
    return message.format(**context)


def load_ini(file_path):
    """加载 ini 配置文件"""
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")
    return config


def download_file(url, output_path):
    try:
        with requests.get(url, stream=True) as response:
            if response.status_code != 200:
                print(translate("download_fail", status_code=response.status_code))
                return False

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
                            print(f"\r{translate('downloading')} {percent_complete:.2f}%", end='')

        print(translate("download_success", output_path=output_path))
        return True
    except Exception as e:
        print(translate("error_occurred", error=e))
        return False


def execute_plugin(plugin_path, function_name, env):
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
            print(translate('func_not_exist'))
            return None
    except Exception as e:
        print(f"{translate('error_occurred')}: {e}")
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
    except Exception:
        return "error"


def lazy_format(str):
    frame = inspect.currentframe().f_back
    context = {**frame.f_globals, **frame.f_locals}

    return str.format(**context)


def process_section(section_name, config):
    release_url = config.get(section_name, "release_url")
    download_url = config.get(section_name, "download_url")
    unzip_folder = lazy_format(config.get(section_name, "unzip_folder"))
    save_path = config.get(section_name, "save_path")
    plugin = os.path.join(current_dir, "utils", config.get(section_name, "plugin"))
    check_version = config.get(section_name, "check_version")
    done = config.get(section_name, "done")
    env = ["save_path", save_path, "ChinaGodMan_U", ChinaGodMan_U]
    # 检查最新版本
    hook_check_version = config.get(section_name, "hook_check_lasted_github", fallback=None)
    if hook_check_version:
        latest_version = execute_plugin(plugin, hook_check_version, env)
    else:
        latest_version = CheckReleaseVersion(release_url)
    print(translate('latest_version'))
    if latest_version is None:
        latest_version = execute_plugin(plugin, check_version, env)

    # 检查本地版本
    local_version = execute_plugin(plugin, check_version, env)
    print(translate('local_version'))
    if local_version is None:
        print(translate('local_version_fail'))
        return
    save_path = lazy_format(save_path)
    if latest_version != local_version:
        print(translate('new_version'))
        download_url = lazy_format(download_url)
        env = ["save_path", save_path, "latest_version", latest_version, "ChinaGodMan_U", ChinaGodMan_U, "unzip_folder", unzip_folder]
        hook_down = config.get(section_name, "hook_download", fallback=None)
        if hook_down:
            download_url = execute_plugin(plugin, hook_down, env)
        print(translate('download_url'))
        if download_file(download_url, save_path):
            execute_plugin(plugin, done, env)
    else:
        print(translate('up_to_date'))


# 初始化
ChinaGodMan_U = os.getenv("ChinaGodMan_U", "C:")
temp_dir = tempfile.gettempdir()
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
country = get_country()
locales_path = f"{current_dir}\\locales\\{country}"
country = country if os.path.isdir(locales_path) else "en"
messages_path = f"{current_dir}\\locales\\{country}\\messages.json"
messages = load_messages(messages_path)
ini_file_path = f"{current_dir}\\softs.ini"
config = load_ini(ini_file_path)
print(translate("program_title"))
menu = []
for index, section in enumerate(config.sections(), start=1):
    description = config.get(section, "description")
    menu.append([str(index), section, description])

menu.append(["0", translate("menu_exit"), translate("menu_exit")])
# 居中
colalign = ("center", "center", "center")
print(tabulate(menu, headers=[translate("menu_header_num"), translate("menu_header_name"), translate("menu_header_func")],
      tablefmt="fancy_grid", colalign=colalign))

while True:
    choice = input(translate("menu_choose"))
    if choice == "0":
        print(translate("menu_exit"))
        break
    elif choice.isdigit() and 1 <= int(choice) <= len(config.sections()):
        section_name = config.sections()[int(choice) - 1]
        process_section(section_name, config)
    else:
        print(translate("menu_invalid"))
