"""
页面下载器
"""

import os
import uuid
import requests
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from bs4 import BeautifulSoup

tags = ['img', 'embed', 'link', 'script']
attrs = ['src', 'href']
phantomjs_path = './bin/phantomjs'
static_file_path = './app/html_data/'


class WebPageDownloader(object):
    def __init__(self):
        executable_path = phantomjs_path
        self.driver = webdriver.PhantomJS(executable_path=executable_path)
        # implicit wait for 10 sec
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1120, 550)

    def get_html(self, url):
        self.driver.get(url)
        html = self.driver.find_element_by_tag_name('html').get_attribute('outerHTML')
        return html

    def localize(self, url):
        html = self.get_html(url)
        return localize(url, html)

    def close(self):
        self.driver.close()


def localize(url, html, key=None):
    soup = BeautifulSoup(html)

    if not key:
        try:
            key = soup.find('title').string.strip()
        except AttributeError:
            key = uuid.uuid4()

    file_dir_name = key + '_files/'
    file_path = static_file_path + file_dir_name
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    resource_elems = soup.find_all(tags)
    for resource_elem in resource_elems:
        for attr in attrs:
            resource_url = resource_elem.get(attr, None)
            if resource_url:
                resource_url = urljoin(url, resource_url)
                try:
                    r = requests.get(resource_url)
                except:
                    continue
                filename = r.headers.get('Content-Disposition',
                                         urlparse(resource_url).path.split('/')[-1])
                with open(file_path + filename, 'wb') as f:
                    f.write(r.content)
                resource_elem[attr] = './' + file_dir_name + filename
    with open(static_file_path + key + '.htm', 'wb') as f:
        f.write(soup.prettify().encode('utf-8'))
    return key

if __name__ == '__main__':
    wd = WebPageDownloader()
    # wd.localize('http://news.cqut.edu.cn/Home/Topic/f260752f-ee08-4117-9ec5-72a612cec629')
    wd.localize('http://www.gszfcg.gansu.gov.cn/web/article/128/0/index.html')
    wd.close()
