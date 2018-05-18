#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
from django.core.paginator import Page
"""
提供简单的爬虫功能.

Authors: liangxuanran@baidu.com
Date: 2018/01/16 15:24:20
"""

import time
import re
import os

import logging
import threading

import url_pool
import page


class Spider(object):
    """多线程爬虫

        实现多线程抓取符合要求的网页

    Attributes:
        conf: 爬虫配置.
        pool: 爬虫任务队列
        prog: url筛选正则表达式
    """ 

    def __init__(self, config):
        self.conf = config
        self.pool = url_pool.TaskPool()
        page.Page.crawl_timeout = self.conf.crawl_timeout
        page.Page.save_path = self.conf.output_directory

    def run(self):
        """运行多个线程执行爬虫工作.
        """
        self.load_url_seed()
        self.mkdir()
        self.prog = re.compile(self.conf.target_url) # 加载url筛选正则表达式
        for i in xrange(self.conf.thread_count):
            t = threading.Thread(target=self._spider_worker, args=(i, self.pool))
            t.setDaemon(True)
            t.start()
        self.pool.join() # 所有爬虫任务完成后退出

    def _spider_worker(self, id, pool):
        """爬虫工作.

        Args:
            id: 数字,标记第几个线程的工作.
        """
        while True:
            new_page = self._get_link(pool)
            if new_page is not None:
                logging.info("thread: %s   crawl  %s", str(id), new_page.url)
                print new_page.url
                links = new_page.get_all_link()
                for link in links:
                    self._update_link(link, new_page.depth, pool)
            pool.task_done() # 当前爬虫任务完成
            time.sleep(self.conf.crawl_interval)

    def _update_link(self, url, depth, pool):  
        """向队列中添加新的待爬取链接.

        Args:
            url: 字符,表示带爬取网页链接.
            depth: 数字,表示链接深度，当大于置顶深度时不再向队列添加.
        """
        if depth < self.conf.max_depth:
            if self.prog.match(url):
                pool.put(page.Page(url, depth + 1))

    def _get_link(self, pool):
        """向队列中取出待爬取链接.

        Returns:
                      返回取出的待爬取链接. 
        """
        new_page = pool.get() 
        return new_page        

    def load_url_seed(self):
        """加载种子url，种子url的文件位置由配置文件标识.
        """
        url_seeds = list()
        try:
            with open(self.conf.url_list_file, "r") as url_seeds_file:
                for line in url_seeds_file:
                    url = line.strip()
                    url_seeds.append(url)
        except IOError:
            logging.warning('open file [%s] failed.' % (self.url_seeds_path))
        for url in url_seeds:
            self.pool.put(page.Page(url, 0))

    def mkdir(self):
        """创建输出文件夹.
        """
        try:
            path = self.conf.output_directory
            path = path.strip()
            path = path.rstrip("\\")
            isExists = os.path.exists(path)
            if not isExists:
                os.makedirs(path)  
        except IOError:
            logging.warning('init dir [%s] failed.' % (self.output_directory))    
