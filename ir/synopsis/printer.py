"""
打印摘要树
"""


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
        output = '{}{}/'.format(indent, node.name)
        if show_vector:
            output += ' ' + str(node.stats.get_feature_vector())
        print(output)


def get_node_by_label_sequence(root, label_sequence):
    """
    根据标签序列从摘要树中获取对应的结点
    :param root: 摘要树根结点
    :param label_sequence: 标签序列
    :return: 对应的结点
    """
    nodes = [root]
    ret_node = root
    for label in label_sequence:
        for node in nodes:
            if node.stats.tag_name.lower() == label.lower():
                nodes = node.children
                ret_node = node
                break
    return ret_node
