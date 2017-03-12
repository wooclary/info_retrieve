"""
数据模型相关
"""
from sklearn.externals import joblib
from .train_and_test import convert2array, get_max_value_index
from .data_set import generate_data_set, get_data_set_from_html_str
from .train_and_test import train_model, get_node_by_index
from ir.synopsis.printer import get_node_by_selector_sequence
from tagger.app.util import align_anchor_for_sequence


model_file_name = 'model.pkl'


def predict(page, align=False):
    sample, root = get_data_set_from_html_str(page)
    # output_c 是 ndarray
    output_c = model.predict(convert2array(sample))
    s = sum(output_c)
    # 下面这段废话...but 就留着吧
    # 先用分类来预测，若仅有一个正类，则采纳
    if s == 1:
        index = list(output_c).index(1)
    # 否则使用最大概率进行预测，选最大概率的node为正类
    else:
        output_p = model.predict_proba(sample)
        index = get_max_value_index(output_p[0::, 1])
    target_node = get_node_by_index(root, index)
    sequence = target_node.name
    # 校准
    if align:
        sequence = align_anchor_for_sequence(sequence)
        target_node = get_node_by_selector_sequence(root, sequence.split(' > '))
    elements = [stat_node.ref for stat_node in target_node.corresponding_ele]
    return elements, sequence


def save_model(clf):
    joblib.dump(clf, model_file_name)


def load_model():
    return joblib.load(model_file_name)


def get_model():
    try:
        clf = load_model()
    except:
        clf = train_model(generate_data_set())
        save_model(clf)
    return clf


def update_model():
    clf = get_model()
    save_model(clf)


# 模型
model = get_model()
