"""
打印摘要树
"""

from ir.html_tag import normalize_selector_str, get_selector


def depth_first_traverse(node, depth):
    """
    深度优先遍历摘要树
    :param node: 摘要树结点
    :param depth: 当前深度
    :return: (结点, 深度)
    """
    yield node, depth
    for child in node.children:
        yield from depth_first_traverse(child, depth+1)


def synopsis_tree_printer(root, show_vector=False):
    """
    打印出摘要树的结构
    :param root: 树的根结点
    :param show_vector: 是否显示模型向量
    """
    for node, depth in depth_first_traverse(root, 0):
        indent = ' ' * 4 * depth
        tag, classes = node.stats.tag_name, node.stats.classes
        selector = get_selector(tag, classes)
        output = '{}{}/'.format(indent, selector)
        if show_vector:
            output += ' ' + str(node.stats)
        print(output)


def get_node_by_selector_sequence(root, selector_sequence):
    """
    根据选择器序列从摘要树中获取对应的结点
    :param root: 摘要树根结点
    :param selector_sequence: [标签序列]
    :return: 对应的结点
    """
    nodes = [root]
    ret_node = root
    for selector in selector_sequence:
        normalize_selector = normalize_selector_str(selector)
        for node in nodes:
            node_selector = get_selector(node.stats.tag_name, node.stats.classes)
            if node_selector.lower() == normalize_selector.lower():
                nodes = node.children
                ret_node = node
                break
    return ret_node
