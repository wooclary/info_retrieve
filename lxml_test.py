#!/usr/bin/env python3

from bs4 import BeautifulSoup

with open("./html_data/重庆市招标投标综合网_招标公告.htm", 'rb') as f:
    unicode_str = f.read().decode()
    soup = BeautifulSoup(unicode_str, 'lxml')
    print([content.name for content in soup.contents])
    print(type(soup.contents[1]))

