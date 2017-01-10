"""
工具类
"""

from ir.statistic_tree.build import get_parsed_soup


def generate_insert_content(file_path):
    """
    由html文件生成用于插入template的html片段
    :param file_path: html文件路径
    :return: 字符串
    """
    soup = get_parsed_soup(file_path, head_filter=True)
    # 去除所有元素的style属性
    stylish_elems = soup.select('[style]')
    for ele in stylish_elems:
        del ele['style']
    return str(soup.html.body)
