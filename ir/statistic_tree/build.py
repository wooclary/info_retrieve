"""
构建统计树
"""


import re
from bs4 import BeautifulSoup

from ir.statistic_tree.node import StatTreeNode


def get_parsed_soup(file_path, parser='html5lib', head_filter=False,
                    iframe_filter=False, script_filter=False):
    """
    输出经过bs4解析后的html文件
    :param file_path: 文件地址
    :param parser: 使用的解析器
    :param head_filter: 是否过滤掉head元素
    :param iframe_filter: 是否过滤掉iframe元素
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
        if head_filter:
            unicode_str = re.sub('<head>[\s\S]*</head>', '', unicode_str)
        if iframe_filter:
            unicode_str = re.sub('<iframe[\s\S]*?>[\s\S]*?</iframe>', '', unicode_str)
        if script_filter:
            unicode_str = re.sub('<script[\s\S]*?>[\s\S]*?</script>', '', unicode_str)

    soup = BeautifulSoup(unicode_str, parser)
    return soup


def get_parsed_soup_from_str(html_content, parser='html5lib', head_filter=False, iframe_filter=False):
    soup = BeautifulSoup(html_content, parser)
    return soup


def get_content_names(soup):
    """
    获得soup.contents中的name列表
    :param soup: bs object
    :return: [names]
    """
    return [content.name for content in soup.contents]


def print_content_names(soup):
    """
    打印soup.contents中的name列表
    :param soup: bs object
    """
    print(get_content_names(soup))


def none_name_children_inspector(soup):
    """
    打印soup.contents中name为none的child
    :param soup:
    """
    print([(i, ctt) for i, ctt in enumerate(soup.contents)
           if ctt.name is None])


def get_not_none_children(soup):
    return [ctt for ctt in soup.contents
            if ctt.name is not None]


def get_not_none_children_names(soup):
    return [ctt.name for ctt in soup.contents
            if ctt.name is not None]


def blank_filter(str_list):
    return [s for s in [s.strip() for s in str_list] if s]


def traverse(stats_node):
    # pre-order
    bs, stats = stats_node.ref, stats_node.stats
    # 元素名
    stats.tag_name = bs.name
    # 类名
    classes = bs.get('class')
    if classes:
        stats.classes = classes  # 若类名不为空，则记录
    # 只属于当前元素的文本的长度
    ele_text = blank_filter(bs.findAll(text=True,
                                       recursive=False))
    stats.char_num = len(''.join(ele_text))
    children = get_not_none_children(stats_node.ref)

    # 需要汇总所有子结点的
    height = 1
    sibling_num = len(children)
    char_sum = stats.char_num

    # 叶子结点的情况
    if not children:
        return height, char_sum

    for child in children:
        # in-order
        # 创建新统计结点
        new_stats_node = StatTreeNode(child)
        # 将新结点加入当前结点的孩子列表中
        stats_node.children.append(new_stats_node)
        # 获取新结点的统计数据对象
        new_stats = new_stats_node.stats
        # 计算根路径距离
        new_stats.root_dist = stats.root_dist + 1
        # 兄弟结点的个数
        new_stats.sibling_num = sibling_num
        # 递归遍历子树, 返回子树高和子树字符数
        child_height, child_char_sum = traverse(new_stats_node)
        # 更新子树高度
        height = max(height, child_height)
        # 更新子树字符数
        char_sum += child_char_sum

    # post-order
    # 子树高度
    height += 1
    stats.subtree_height = height
    # 子树字符数
    stats.char_sum = char_sum
    # 将需要由低向上计算的量, 返回上一层
    return height, char_sum


def build(file_path, parser='html5lib'):
    # output_parsed_page(file_path, parser)
    # 读取文件内容
    soup = get_parsed_soup(file_path, parser)
    # 定位到html根结点
    html = soup.html
    root_node = StatTreeNode(html)

    root_node.stats.sibling_num = 1

    _ = traverse(root_node)

    return root_node


def build_from_str(html, parser='html5lib'):
    # output_parsed_page(file_path, parser)
    # 读取文件内容
    soup = get_parsed_soup_from_str(html, parser)
    # 定位到html根结点
    html = soup.html
    root_node = StatTreeNode(html)

    root_node.stats.sibling_num = 1

    _ = traverse(root_node)

    return root_node
