#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
提供简单的爬虫功能.

Authors: liangxuanran@baidu.com
Date: 2018/01/16 15:24:20
"""
import sys

import ConfigParser
import logging

class SpiderConf(object):
    """spider配置文件
        
              读取配置文件，保存爬虫程序用户设置

        Attributes:
        
            url_list_file: 种子文件路径
            output_directory: 抓取结果存储目录
            max_depth: 最大抓取深度(种子为0级)
            crawl_interval: 抓取间隔. 单位: 秒 
            crawl_timeout: 抓取超时. 单位: 秒
            target_url: 需要存储的目标网页URL pattern(正则表达式) 
            thread_count: 抓取线程数
    """
    
    def __init__(self):
        self.url_list_file = None
        self.output_directory = None
        self.max_depth = 1
        self.crawl_interval = 1
        self.crawl_timeout = 1
        self.target_url = None
        self.thread_count = 1

    def read_config_args(self, path):
        """读取配置文件参数.

        Args:
            path: 字符,表示配置文件路径.

        """
        config = ConfigParser.SafeConfigParser()
        config.read(path)
        section = 'spider'
        if config.has_section(section):
            self.url_list_file = config.get(section, "url_list_file")
            self.output_directory = config.get(section, "output_directory")
            self.max_depth = config.getint(section, "max_depth")
            self.crawl_interval = config.getint(section, "crawl_interval")
            self.crawl_timeout = config.getint(section, "crawl_timeout")
            self.target_url = config.get(section, "target_url")
            self.thread_count = config.getint(section, "thread_count")
        else:
            logging.error('config file [%s] does not have section [%s]' % (path, section))
            sys.exit(1)