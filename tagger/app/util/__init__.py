"""
工具类
"""
import re
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


def generate_injected_content(file_path, css_path, jquery_path, js_path):
    """
    生成注入标注脚本后的HTML字符串
    :param file_path:待注入的HTML文件路径
    :param css_path:注入的css脚本路径
    :param jquery_path:注入的jquery脚本路径
    :param js_path:注入的javascript脚本路径
    :return:注入后的HTML文本
    """
    # 删除所有iframe元素
    soup = get_parsed_soup(file_path, iframe_filter=True, script_filter=True)
    head = soup.find('head')
    if head:
        # 注入顺序不能够改变
        css = soup.new_tag('link', rel="stylesheet", type="text/css", href=css_path)
        head.append(css)
        jquery = soup.new_tag('script', type="text/javascript", src=jquery_path)
        head.append(jquery)
        js = soup.new_tag('script', type="text/javascript", src=js_path)
        head.append(js)
    return str(soup)


def align_anchor_for_sequence(sequence, depth=3):
    """
    校准到a标签的逻辑，用于提取网页链接
    :param sequence: 字符串形式的节点名序列
    :param depth: 距离叶子节点的有效校准深度，默认为3
    :return: 校准后的节点名序列
    """
    seq_list = sequence.split(' > ')
    last_three_items_tag = [item.split('.')[0] for item in seq_list[-depth:]]
    length = len(last_three_items_tag)
    if 'a' in last_three_items_tag:
        index = last_three_items_tag.index('a')
        right_offset = length - index - 1
        return ' > '.join(seq_list[:-right_offset if right_offset != 0 else None])
    return sequence


def align_anchor_for_sel(selector, depth=3):
    selector = selector.split(' > ')
    last_three_items_tag = [re.split('\[[\s\S]*?\]', item)[0].split(':not')[0].split('.')[0]
                            for item in selector[-depth:]]
    length = len(last_three_items_tag)
    if 'a' in last_three_items_tag:
        index = last_three_items_tag.index('a')
        right_offset = length - index - 1
    return ' > '.join(selector[:-right_offset if right_offset != 0 else None])


def label_sequence2css_selector(sequence):
    """
    节点名序列转换成css选择器
    :param sequence:节点名序列字符串
    :return:css选择器字符串
    """
    sequence = sequence.split(' > ')
    for i, node_name in enumerate(sequence):
        if node_name == 'html':
            continue
        name_list = node_name.split('.')
        if len(name_list) == 1:
            sequence[i] += ':not([class])'
        else:
            sequence[i] = (name_list[0] +
                           "[class='" +
                           ' '.join(name_list[1:]) +
                           "']")

    return ' > '.join(sequence)


def decode_html_file(file_path):
    """
    解码HTML
    :param file_path: HTML文件路径
    :return: HTML unicode str
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
        # 先用utf-8解码以获取charset
        utf8_content = file_content.decode(encoding='utf-8',
                                           errors='ignore')
        m = re.search(r'<meta.*?charset=([^"\']+)',
                      utf8_content)
        # 若匹配到charset则使用否则默认utf-8
        encoding = m.group(1) if m else 'utf-8'
        unicode_str = file_content.decode(encoding=encoding,
                                          errors='ignore')
    return unicode_str