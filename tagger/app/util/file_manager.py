"""
用于Tagger的文件管理器
"""
import os
import threading
import json


class FileManager(object):
    def __init__(self, app=None):
        self._app = None
        script_path = os.path.dirname(os.path.realpath(__file__))
        self._dir = os.path.join(script_path, '../html_data')
        self._ext = '.htm'
        self._file_list = []
        self._relative_dir = 'html_data/'
        self._result = os.path.join(script_path, '../result/tag_result.txt')
        self._lock = threading.Lock()
        self._result_lock = threading.Lock()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._app = app
        self._dir = app.config['DATA_PATH'] or ''
        self._relative_dir = app.config['DATA_EXTRA'] or ''
        self._result = app.config['RESULT_FILE'] or ''
        self._ext = app.config['DATA_EXT'] or '.txt'

    def get_file_list(self, has_ext=True):
        file_list = []
        for file in os.listdir(self._dir):
            if file.endswith(self._ext):
                file_list.append(file)
        # 加锁,更新列表
        self._lock.acquire()
        try:
            self._file_list = file_list
        finally:
            self._lock.release()
        if has_ext:
            return file_list
        else:
            return [os.path.splitext(file)[0] for file in file_list]

    def get_filename_list(self):
        if not self._file_list:
            self.get_file_list()
        return [os.path.splitext(f)[0] for f in self._file_list]

    def get_file_path(self, filename, has_ext=False, update=False):
        if not self._file_list or update:
            self.get_file_list()
        if not has_ext:
            filename += self._ext
        if filename in self._file_list:
            return os.path.join(self._dir, filename)
        else:
            return None

    def search_file_path(self, path):
        full_path = os.path.join(self._dir, path)
        ret_path = None
        if os.path.isfile(full_path):
            ret_path = os.path.join(self._relative_dir, path)
        return ret_path

    def write_result(self, file, labels, sel):
        self._result_lock.acquire()
        with open(self._result, 'r') as f:
            result = json.loads(f.read())

        with open(self._result, 'w') as f:
            result[file] = {'label': labels, 'sel': sel}
            f.write(json.dumps(result))
        self._result_lock.release()

    def get_result(self):
        with open(self._result, 'r') as f:
            result = json.loads(f.read())
        return result
