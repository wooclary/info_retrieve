"""
构建路径摘要
"""


from collections import deque

from ir.synopsis.node import SynopsisNode
from ir.html_tag import get_selector, parse_selector


class Queue(deque):
    def add(self, *x):
        self.extend(x)

    def pop(self):
        return self.popleft()


def build(stats_tree_root):
    """
    基于统计树构造摘要树
    :param stats_tree_root:
    :return: 摘要树根结点, 索引
    """
    # 接收 (node, parent_selector, level) 三元组
    q = Queue([(stats_tree_root, '', 0)])
    # 摘要树的层次索引 [{selector: synopsis_node}]
    level_index = []

    # 广度优先遍历
    while q:
        # 出队
        node, parent_selector, level = q.pop()
        # print(parent_selector)
        # if parent_selector == 'div.ztb_list_right':
        #     print('hahha')
        tag = node.stats.tag_name
        classes = node.stats.classes
        selector = get_selector(tag, classes)
        selector_sequence = parent_selector + ' > ' + selector if parent_selector else selector
        # 操作
        synopsis_node = None
        # 若开始遍历新的一层
        if len(level_index) <= level:
            # 创建新的摘要结点，并更新index
            synopsis_node = SynopsisNode(selector_sequence)
            level_index.append({selector_sequence: synopsis_node})
            synopsis_node.add_corresponding_ele(node)
        else:
            index = level_index[level]
            # 若该结点标签对应的摘要结点已存在
            if selector_sequence in index:
                # 直接将结点添加在摘要结点下
                index[selector_sequence].add_corresponding_ele(node)
            else:
                # 否则创建新的摘要结点
                synopsis_node = SynopsisNode(selector_sequence)
                index[selector_sequence] = synopsis_node
                synopsis_node.add_corresponding_ele(node)
        # 若在非0的层创建了新的摘要结点, 则更新其parent的children列表
        if level and synopsis_node:
            parent_synopsis_node = level_index[level-1][parent_selector]
            parent_synopsis_node.add_child(synopsis_node)

        # 入队
        # 为所有子结点构造 (node, parent_selector, level) 三元组
        child_items = [(child, selector_sequence, level+1) for child in node.children]
        q.add(*child_items)

    # 对生成的树的每个结点进行计算
    calculate(level_index)
    # 返回摘要树的根结点及索引
    return list(level_index[0].values())[0], level_index


def calculate(level_index):
    """
    对摘要树每个结点进行值的计算
    :param level_index: 摘要树索引
    """
    tree_height = len(level_index)
    for level in level_index:
        for selector_sequence, synopsis in level.items():
            elems = synopsis.corresponding_ele
            # 解析selector
            selector = selector_sequence.split(' > ')[-1]  # 取序列最后一个选择器
            tag, classes = parse_selector(selector)
            # 获取摘要结点数据
            stats = synopsis.stats
            # 设置标签
            stats.tag_name = tag
            # 设置类
            stats.classes = classes
            # 当前元素的平均字符数
            stats.current_elem_char_num_avg = cal_avg('char_num', elems)
            # 子树的平均字符总数
            stats.subtree_char_sum_avg = cal_avg('char_sum', elems)
            # 字符比(加1是为了防止分母为0)
            stats.char_rate = \
                ((stats.current_elem_char_num_avg+1)/(stats.subtree_char_sum_avg+1))
            # 根路径距离
            stats.root_dist = cal_avg('root_dist', elems)
            # 子树平均树高
            stats.subtree_height_avg = cal_avg('subtree_height', elems)
            # 局部平均高度比
            stats.local_height_rate = cal_avg_rate('root_dist', 'subtree_height', elems)
            # 全局高度比
            stats.gloabl_height_rate = cal_avg('root_dist', elems) / tree_height
            # 平均兄弟结点数
            stats.avg_sibling_num = cal_avg('sibling_num', elems)
            # TODO 添加判断是否为同质结点的逻辑
            stats.is_homogeneous = False
            # TODO 添加是否为同构结点的逻辑(即同质的基础上, 每个子标签的度也相同)
            stats.is_isomorphic = False


def cal_avg(stat_name, elements):
    n = len(elements)
    s = 0
    for elem in elements:
        s += getattr(elem.stats, stat_name)
    return s/n


def cal_avg_rate(name_one, name_two, elements):
    """
    对elements每个元素计算 one/(one+two) 并求平均
    :param name_one: one的属性名
    :param name_two: two的属性名
    :param elements: 元素列表
    :return: avg(one/(one+two))
    """
    n = len(elements)
    s = 0
    for elem in elements:
        stats = elem.stats
        one = getattr(stats, name_one)
        two = getattr(stats, name_two)
        s += one / (one + two)
    return s/n
