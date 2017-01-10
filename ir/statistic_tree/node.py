"""
统计树结点
"""


class Stats(object):
    def __init__(self, tag_name='', char_num=0, char_sum=0,
                 root_dist=0, subtree_height=0, sibling_num=0):
        self.tag_name = tag_name  # html元素标签名
        self.char_num = char_num  # 当前元素内的字符数
        self.char_sum = char_sum  # 当前元素的子树的字符数和
        self.root_dist = root_dist  # 从html根结点到该结点的距离
        self.subtree_height = subtree_height  # 当前元素的子树高度
        self.sibling_num = sibling_num  # 兄弟结点的数量

    def __str__(self):
        vector = [self.char_num, self.char_sum, self.root_dist,
                  self.subtree_height, self.sibling_num]
        return '(' + ', '.join([str(vi) for vi in vector]) + ')'


class StatTreeNode(object):
    """
    用于存放统计值的树的结点
    """

    def __init__(self, ref_bs4_node):
        self.stats = Stats()
        self._children = []  # 子结点列表
        self._ref = ref_bs4_node  # 对应的bs4结点的引用

    @property
    def ref(self):
        return self._ref

    @property
    def children(self):
        """
        获取子结点列表
        :return: [st_node]
        """
        return self._children

    def add_child(self, st_node):
        """
        添加子结点
        :param st_node:
        """
        self._children.append(st_node)
