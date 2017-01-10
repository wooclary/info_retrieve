"""
生成数据集相关
"""

from ir.synopsis.printer import (depth_first_traverse,
                                 get_node_by_label_sequence)
from ir.statistic_tree.build import build as build_stats
from ir.statistic_tree.printer import stats_tree_printer
from ir.synopsis.build import build as build_synopsis
from ir.synopsis.printer import synopsis_tree_printer
from tagger.app.util.file_manager import FileManager


fm = FileManager()


def get_data_set_from_html(file_name):
    """
    从html文件生成数据集
    :param file_name: html文件名
    :return: 对应的数据集
    """
    file_path = fm.get_file_path(file_name)
    tree_root = build_stats(file_path)
    # stats_tree_printer(tree_root, True)
    synopsis_root, level_index = build_synopsis(tree_root)
    # synopsis_tree_printer(synopsis_root, True)
    tag_result = fm.get_result()
    target_node_labels = tag_result[file_name].split(' > ')
    target_node = get_node_by_label_sequence(synopsis_root,
                                             target_node_labels)
    data = []
    for node, _ in depth_first_traverse(synopsis_root, 0):
        feature = node.stats.get_feature_vector()
        cls = 1 if node == target_node else 0
        # 将分类放在最后一行
        feature.append(cls)
        data.append(feature)
    return data


def generate_data_set_for_loocv():
    """
    为留一验证(loocv)生成数据集
    :return: (训练集, 测试集）
    """
    file_list = fm.get_file_list(has_ext=False)
    for test_file in file_list:
        # 此处并不去掉列标号，便于验证
        test_data = get_data_set_from_html(test_file)
        remain = [file for file in file_list if file != test_file]
        train_data = []
        for train_file in remain:
            train_data += get_data_set_from_html(train_file)
        yield train_data, test_data
