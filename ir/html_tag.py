"""
Html Tag 相关
"""

import os


class HtmlTagMap(object):
    def __init__(self, file):
        with open(file, 'r') as f:
            tags = f.read().split('\n')
        self._map = {tag: i for i, tag in enumerate(tags)}
        self._num = len(tags)

    def get_index(self, tag):
        return self._map.get(tag, None)

    def get_num(self):
        return self._num

# 创建tag_map
path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                    'all_valid_html_tag.txt')
tag_map = HtmlTagMap(path)


def parse_selector(selector_str):
    """
    将选择器字符串转换结构化数据
    例如: 'div.tbox.ftbox' -> ['div', 'tbox', 'ftbox']
    :param selector_str: 选择器字符串
    :return: tag, classes
    """
    selectors = selector_str.split('.')
    tag, classes = selectors[0], selectors[1:]
    # 将class按字典顺序排序
    classes.sort()
    return tag, classes


def get_selector(tag, classes):
    """
    根据tag和classes生成选择器字符串
    例如: 'div', ['tbox', 'ftbox'] -> 'div.tbox.ftbox'
    :param tag: 标签
    :param classes: 类名
    :return: 选择器字符串
    """
    cls_part = '.'.join(classes)
    return tag + '.' + cls_part if cls_part else tag


def normalize_selector_str(selector_str):
    """
    标准化选择器字符串，使类别按字典序排列
    :param selector_str: 选择器字符串
    :return: 标准化的选择器字符串
    """
    tag, classes = parse_selector(selector_str)
    return get_selector(tag, classes)
