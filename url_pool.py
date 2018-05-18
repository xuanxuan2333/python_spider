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
import Queue
import logging


class TaskPool(Queue.PriorityQueue):
    """爬虫任务队列

              所有爬虫工作线程从爬虫任务队列取任务，并把爬到的链接添加到任务队列

        Attributes:

            url_set: 结构用来进行链接去重的set结构
    """

    def _init(self, maxsize=0):
        Queue.PriorityQueue._init(self, maxsize)
        self.url_set = set() # set结构用来进行链接去重

    def _put(self, node):

        if node.url not in self.url_set: # 当链接已存在时忽略
            Queue.PriorityQueue._put(self, node)
            self.url_set.add(node.url)
            logging.info('node %s putted', str(node))
        else:
            self.unfinished_tasks -= 1  # 每调用一次put, unfinished_tasks就会加1, 所以要先减去1
