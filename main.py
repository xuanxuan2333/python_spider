#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved (conflict try)
#
################################################################################
from src.spider_conf import SpiderConf
"""
提供简单的爬虫功能.

Authors: liangxuanran@baidu.com
Date: 2018/01/16 15:24:20
"""
import argparse

import spider
import spider_conf


def main():
    """入口函数
    """
    path = read_arg()
    config = spider_conf.SpiderConf()
    config.read_config_args(path)
    my_spider = spider.Spider(config)
    my_spider.run()


def read_arg():
    """读取arg参数，支持命令行参数处理。具体包含: -h(帮助)、-v(版本)、-c(配置文件).
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='spider v1.0')
    parser.add_argument('-c', '--conf', nargs=1, type=str, default='./conf', \
                        help='Specify config file path')
    args = parser.parse_args()
    return args.conf


if __name__ == '__main__':
    main()     
