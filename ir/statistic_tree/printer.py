"""
打印统计树
"""


def depth_first_traverse(node, depth):
    yield node, depth
    for child in node.children:
        yield from depth_first_traverse(child, depth+1)


def stats_tree_printer(root, show_vector=False):
    """
    打印出统计树的结构
    :param root: 树的根结点
    :param show_vector: 是否显示模型向量
    """
    for node, depth in depth_first_traverse(root, 0):
        indent = ' ' * 4 * depth
        output = '{}{}/'.format(indent, node.stats.tag_name)
        if show_vector:
            output += ' ' + str(node.stats)
        print(output)


if __name__ == '__main__':
    pass
