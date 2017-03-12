#!/usr/bin/env python3

from tagger.app.util.file_manager import FileManager
from ir.statistic_tree.build import build as build_stats
from ir.statistic_tree.printer import stats_tree_printer
from ir.synopsis.build import build as build_synopsis
from ir.synopsis.printer import synopsis_tree_printer


fm = FileManager()
file_path = fm.get_file_path("重庆市招标投标综合网_招标公告")
tree_root = build_stats(file_path)
stats_tree_printer(tree_root, True)
synopsis_root, level_index = build_synopsis(tree_root)
synopsis_tree_printer(synopsis_root, True)
print('end')
