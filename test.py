from ir.statistic_tree.build import build as build_stats
from ir.statistic_tree.printer import stats_tree_printer
from ir.synopsis.build import build as build_synopsis
from ir.synopsis.printer import synopsis_tree_printer
from ir.model.train_and_test import cross_validate

# tree_root = build_stats("./tagger/app/html_data/重庆市招标投标综合网_招标公告.html")
# stats_tree_printer(tree_root, True)
# synopsis_root, level_index = build_synopsis(tree_root)
# synopsis_tree_printer(synopsis_root, True)
cross_validate()
