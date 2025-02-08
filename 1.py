import locale


def get_full_country_code():
    """
    获取当前系统的完整国家代码，例如 'zh_CN' 表示中文（中国）
    """
    locale_info = locale.getdefaultlocale()
    if locale_info and locale_info[0]:
        return locale_info[0]
    return None


# 调用示例

print("完整的国家代码：", full_country_code)
