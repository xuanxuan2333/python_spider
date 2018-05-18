#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
from src.spider_conf import SpiderConf
"""
提供简单的爬虫功能.

Authors: liangxuanran@baidu.com
Date: 2018/01/16 15:24:20
"""
import unittest

import spider_conf
import spider
import os


class SpiderTest(unittest.TestCase):
    """spider单元测试
    """

    def setUp(self):
        self.inputfile = "./urls"
        self.outputfile = "./output"
        self.conf = spider_conf.SpiderConf()
        self.conf.url_list_file = self.inputfile
        self.conf.output_directory = self.outputfile
        self.conf.max_depth = 1
        self.conf.crawl_interval = 1
        self.conf.crawl_timeout = 5
        self.conf.target_url = ".*.(htm|html)$"
        self.conf.thread_count = 4
        try:
            file_object = open(self.inputfile, 'w')
            file_object.write("http://pycm.baidu.com:8081")
            file_object.close()
        except IOError:
            print "write file %s failed." % self.inputfile

    def test_spider(self):
        my_spider = spider.Spider(self.conf)
        my_spider.run()

        list = os.listdir(self.outputfile) #列出目录下的所有文件和目录

        test_output = set(list)

        expected_output = set()

        expected_output.add(converse("http://pycm.baidu.com:8081"))
        expected_output.add(converse("http://pycm.baidu.com:8081/page1.html"))
        expected_output.add(converse(" http://pycm.baidu.com:8081/page2.html"))
        expected_output.add(converse(" http://pycm.baidu.com:8081/page3.html"))
        expected_output.add(converse("http://pycm.baidu.com:8081/mirror/index.html"))
        expected_output.add(converse(" http://pycm.baidu.com:8081/page4.html"))

        self.assertSetEqual(test_output, expected_output)


def converse(self, url_name):
    url_name = url_name.replace(":", "_")
    url_name = url_name.replace("/", "_")
    url_name = url_name.replace("\\", "_")
    url_name = url_name.replace(".", "_")
    if not url_name.endswith(".htm"):
        url_name = url_name + ".htm"  # 添加文件名后缀
    return url_name            


if __name__ == "__main__":
    import sys
    sys.argv = ['', 'SpiderTest.test_spider']
    unittest.main()
