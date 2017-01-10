"""
路径摘要结点
"""
from ir.html_tag import tag_map


class SynopsisStats(object):
    def __init__(self):
        # 标签名
        self.tag_name = ''
        # 当前元素的平均字符数
        self.current_elem_char_num_avg = 0
        # 子树的平均字符总数
        self.subtree_char_sum_avg = 0
        # 字符比 = 前两者加一之比
        self.char_rate = 0
        # 根路径距离
        self.root_dist = 0
        # 子树平均树高
        self.subtree_height_avg = 0
        # 局部平均高度比 = root_dist / root_dist+subtree_height
        self.local_height_rate = 0
        # 全局高度比 = root_dist / tree_height
        self.gloabl_height_rate = 0
        # 平均兄弟结点数
        self.avg_sibling_num = 0
        # 是否为同质结点
        self.is_homogeneous = False
        # 是否为同构结点
        self.is_isomorphic = False

    def get_feature_vector(self):
        index = tag_map.get_index(self.tag_name)
        one_hot = [0 for _ in range(tag_map.get_num())]
        # 若有此标签，则标记，否则忽略
        if index is not None:
            one_hot[index] = 1
        return one_hot + self.get_vector()

    def get_vector(self):
        return [self.current_elem_char_num_avg,
                self.subtree_char_sum_avg, self.char_rate,
                self.root_dist, self.subtree_height_avg,
                self.local_height_rate, self.gloabl_height_rate,
                self.avg_sibling_num, int(self.is_homogeneous),
                int(self.is_isomorphic)]

    def __str__(self):
        vector = self.get_vector()
        return '(' + self.tag_name + ', ' +\
               ', '.join([str(vi) for vi in vector]) + ')'


class SynopsisNode(object):
    """
    用于存放统计值的摘要结点
    """
    def __init__(self, name):
        self.name = name
        self.stats = SynopsisStats()
        self._children = []
        self._corresponding_elements = []

    @property
    def children(self):
        """
        获取子结点列表
        :return: [s_node]
        """
        return self._children

    @property
    def corresponding_ele(self):
        return self._corresponding_elements

    def add_corresponding_ele(self, node):
        self._corresponding_elements.append(node)

    def add_child(self, s_node):
        """
        添加子结点
        :param s_node:
        """
        self._children.append(s_node)
