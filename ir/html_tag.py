"""
Html Tag
"""


class HtmlTagMap(object):
    def __init__(self, file):
        with open(file, 'r') as f:
            tags = f.read().split('\n')
        self._map = {tag: i for i, tag in enumerate(tags)}
        self._num = len(tags)

    def get_index(self, tag):
        return self._map.get(tag, None)

    def get_num(self):
        return self._num

tag_map = HtmlTagMap('./ir/all_valid_html_tag.txt')
