import os
from flask import (request, render_template, send_from_directory,
                   abort, jsonify)

from app import file_manager
from app.util import generate_insert_content
from . import main


@main.route('/', methods=['GET'])
def home():
    file_names = file_manager.get_filename_list()
    temp = render_template('interface', file_names=file_names)
    print(temp)
    return temp


@main.route('/panel', methods=['GET', 'POST'])
def panel():
    file_name = request.args.get('filename', None)
    if request.method == 'POST':
        result = request.get_json(force=True, silent=True)
        if result is not None:
            label_sequence = result.get('label_sequence', None)
            try:
                file_manager.write_result(file_name, label_sequence)
            except:
                return jsonify(result='fail', status=400)
            else:
                return jsonify(result='success', status=200)
    else:
        if file_name is None:
            return "<h1>Welcome!</h1>"
        path = file_manager.get_file_path(file_name)
        if path is None:
            abort(404)
        insert_str = generate_insert_content(path)
        return render_template('tag_panel', insert_html_body=insert_str)


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    """
    将所有其它路由都指向这里，用于处理被插入的HTML的相关请求
    :param path: 其它路径
    :return:资源文件
    """
    result = file_manager.search_file_path(path)
    if result is None:
        abort(404)
    head_path, tail_name = os.path.split(result)
    return send_from_directory(head_path, tail_name)
