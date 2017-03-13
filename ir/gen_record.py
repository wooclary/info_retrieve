"""
生成结构化数据相关
"""

import lxml.html
from pyquery import PyQuery as pq

from ir.model import predict
from tagger.app.util.file_manager import FileManager
from tagger.app.util import decode_html_file


fm = FileManager()
rules = fm.get_result()
backward_filter_keywords = ['prev', 'next',
                            'pre', 'nxt',
                            '更多', 'more',
                            '上一页', '下一页',
                            '前页', '后页']


def has_keyword(title):
    flag = False
    for kw in backward_filter_keywords:
        if kw in title:
            flag = True
            break
    return flag


def gen(page, key='', from_file=False):
    rule = rules.get(key, '')
    if from_file:
        file_path = fm.get_file_path(page)
        page = decode_html_file(file_path)
    if rule:
        doc = pq(page)
        css_sel = rule.get('sel')
        elements = list(doc(css_sel).items())
        records = []
        # 若common css 选择器没有通过PyQuery选出元素
        # 则使用label sequence
        if not elements:
            sequence = rule.get('label')
            elements = list(doc(sequence).items())
        # 若PyQuery使用label无效
        if not elements:
            tree = lxml.html.fromstring(page)
            elements = tree.cssselect(css_sel)
            for element in elements:
                link = element.get('href')
                title = element.text_content().strip()
                if link and title and not has_keyword(title):
                    records.append((title, link))
            return records
        # 一般情况下
        for element in elements:
            link = element.attr('href')
            title = element.text().strip()
            if link and title and not has_keyword(title):
                records.append((title, link))
        return records
    else:
        # 使用模型标注, 参数align=True表示使用校准
        elements, sequence = predict(page, align=True)
        records = []
        # 校准
        for element in elements:
            link = element.get('href', None)
            title = element.text.strip()
            if link and title and not has_keyword(title):
                records.append((title, link))
        return records
