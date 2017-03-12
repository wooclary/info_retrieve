"""
训练与测试
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from ir.synopsis.printer import depth_first_traverse
from ir.model.data_set import generate_data_set_for_loocv
from ir.html_tag import get_selector


def convert2array(data):
    """
    将python list转换成numpy array
    :param data: python list
    :return: numpy array
    """
    data = np.array(data)
    return data


def get_max_value_index(array):
    """
    返回array中最大值的索引
    :param array: 数组数据
    :return: 最大值的索引
    """
    max_value, max_index = 0, -1
    for i, x in enumerate(np.nditer(array)):
        if x > max_value:
            max_index, max_value = i, x
    return max_index


def train_model(train_data):
    """
    训练模型
    :param train_data:
    :return:
    """
    train_data = convert2array(train_data)
    # log_reg = LogisticRegression(class_weight='balanced')
    rfc = RandomForestClassifier(n_estimators=20)
    # log_reg = LogisticRegression()
    rfc.fit(train_data[0::, 0:-1], train_data[0::, -1])
    return rfc


def test_model(test_data, model):
    """
    测试模型效果，最高打分的样本为正例
    :param test_data: 测试数据集
    :param model: 模型
    :return: 测试结果
    """
    test_data = convert2array(test_data)
    output_c = model.predict(test_data[0::, 0:-1])
    # 注意predict_proba返回的是[n_sample, n_classes]尺寸的array
    output_p = model.predict_proba(test_data[0::, 0:-1])
    target_c = test_data[0::, -1]
    # print(output_p)
    # print(output_c)
    # print(target)

    tp, fp, fn, tn = 0, 0, 0, 0
    for cls, target in zip(output_c, target_c):
        if target == 1:
            if cls == 1:
                tp += 1  # 正类被分为正类
            else:
                fn += 1  # 正类被分为负类
        else:
            if cls == 1:
                fp += 1  # 负类被分为正类
            else:
                tn += 1  # 负类被分为负类

    # 按打分最值分类
    max_index = get_max_value_index(output_p[0::, 1])
    max_acc = 1 if target_c[max_index] == 1 else 0
    # node = get_node_by_index(max_index)
    # print(node.stats.tag_name)
    # print(node.stats.classes)
    # print(str(node))
    return tp, fp, fn, tn, max_acc


def cross_validate():
    """
    交叉验证
    :return: 正确率
    """
    tp = fp = fn = tn = max_acc = n = 0
    print('%5s %5s %5s %5s %5s %5s' % ('n', 'tp', 'fp', 'fn', 'tn', 'max_acc'))
    for train_data, test_data in generate_data_set_for_loocv():
        model = train_model(train_data)
        _tp, _fp, _fn, _tn, _max_acc = test_model(test_data, model)
        print('%5d %5d %5d %5d %5d %5d' % (n, _tp, _fp, _fn, _tn, _max_acc))
        tp += _tp
        fp += _fp
        fn += _fn
        tn += _tn
        max_acc += _max_acc
        n += 1
    accuracy = (tp+tn)/(tp+tn+fp+fn)
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    max_accuracy = max_acc/n
    output = ("准确率：%f\n精确率：%f\n召回率：%f\n最大值方法准确率：%f" %
              (accuracy, precision, recall, max_accuracy))
    print(output)


def get_node_by_index(root, index):
    n = 0
    for node, depth in depth_first_traverse(root, 0):
        if n == index:
            return node
        n += 1
