"""
路由视图
"""

import os
import requests
from flask import (request, render_template, send_from_directory,
                   abort, jsonify, url_for, session, redirect)

from ir.model import predict
from app import file_manager
from app.util import (generate_injected_content, align_anchor_for_sequence,
                      align_anchor_for_sel, decode_html_file)
from app.util.page_fetcher import WebPageDownloader
from . import main
from .forms import SearchForm, CheckForm


@main.route('/', methods=['GET', 'POST'])
def home():
    search_form = SearchForm()
    check_form = CheckForm()
    if search_form.validate_on_submit():
        url = search_form.url.data
        search_form.url.data = ''
        res = requests.get(url)
        if res.status_code < 400:
            # Web site exists
            try:
                wd = WebPageDownloader()
                title = wd.localize(url)
                session['current_page'] = title
                wd.close()
            except Exception as e:
                print(str(e))
                abort(404)
        return redirect(url_for('main.tags'))
        # else:
        #     abort(404)
    if check_form.validate_on_submit():
        session['current_page'] = ''
        return redirect(url_for('main.tags'))
    return render_template('index',
                           search_form=search_form,
                           check_form=check_form)


@main.route('/tags', methods=['GET'])
def tags():
    current_page = session.get('current_page', '')
    if current_page:
        file_names = [current_page]
    else:
        file_names = file_manager.get_filename_list()
    return render_template('interface', file_names=file_names)


@main.route('/panel', methods=['GET', 'POST'])
def panel():
    file_name = request.args.get('filename', None)
    if request.method == 'POST':
        result = request.get_json(force=True, silent=True)
        if result is not None:
            label_sequence = result.get('label_sequence', None)
            aligned_label_sequence = align_anchor_for_sequence(label_sequence)
            sel = result.get('common', None)
            aligned_sel = align_anchor_for_sel(sel)
            try:
                file_manager.write_result(file_name,
                                          aligned_label_sequence,
                                          aligned_sel)
            except:
                return jsonify(result='fail', status=400)
            else:
                return jsonify(result='success', status=200)
    else:
        if file_name is None:
            return "<h1>Welcome!</h1>"
        path = file_manager.get_file_path(file_name, update=True)
        if path is None:
            abort(404)
        # insert_str = generate_insert_content(path)
        # return render_template('tag_panel', insert_html_body=insert_str)
        return generate_injected_content(
            path,
            url_for('static', filename='css/tag_panel.css'),
            url_for('static', filename='scripts/tag_panel.jquery.js'),
            url_for('static', filename='scripts/tag_panel.js')
        )


@main.route('/rule', methods=['GET'])
def rule():
    file_name = request.args.get('filename', '')
    # 若file_name为空，或不存在于本地文件，则抛出404
    if not(file_name and
            file_name in file_manager.get_filename_list()):
        abort(404)
    result = file_manager.get_result()
    rule = result.get(file_name, '')
    label_sequence, css_selector = '', ''
    is_rec = False
    # 若已经有人工标注，则读取
    if rule:
        label_sequence = rule.get('label', '')
        css_selector = rule.get('sel', '')
    else:
        is_rec = True
        file_path = file_manager.get_file_path(file_name)
        page = decode_html_file(file_path)
        _, label_sequence = predict(page, align=True)
    # TODO 整合模型推荐
    # is_rec表示是否为
    return jsonify(is_rec=is_rec, seq=label_sequence, sel=css_selector)


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
        # 这里不能用abort，否则会返回自定义的错误页
        return '', 404
    head_path, tail_name = os.path.split(result)
    return send_from_directory(head_path, tail_name)
