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
import re

import urllib2  
import urlparse
import logging

import bs4

class Page(object):
    """spider配置文件
        
              读取配置文件，保存爬虫程序用户设置

        Attributes:
        
            crawl_timeout: 爬虫超时时间
            save_path: 页面保存路径
            url: 页面url地址
            depth: 页面深度
    """
    crawl_timeout = 60
    save_path = "./"
    
    
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth

    def get_all_link(self):
        """获取网页中的所有链接，通过urllib2下载网页，BeautifulSoup解析页面，urlparse进行连接解析.

        Returns:
                      返回网页中的所有链接. 
        """
        links = list()
        try:
            page = urllib2.urlopen(self.url, timeout=self.crawl_timeout).read()
            self._write(self.url, page)
            bsObj = bs4.BeautifulSoup(page, "html.parser")  
            for link in bsObj.findAll("a"):
                if 'href' in link.attrs and link.attrs['href'] is not None:  
                    internalLink = urlparse.urljoin(self.url, link.attrs['href']) # 兼容相对路径链接
                    if internalLink.startswith("javascript:"):
                        js_link = prog.search(internalLink)
                        if js_link is not None:
                            internalLink = urlparse.urljoin(self.url, js_link.group(0)) # 兼容js链接
                    links.append(internalLink)
        except urllib2.URLError as e:  
            logging.warning(e.reason)   
        except urllib2.HTTPError as e:  
            logging.warning(e.code)  
            logging.warning(e.read()) 
        return links
    
    def _write(self, url_name, all_the_text):
        """将下载的网页保存到指定路径.
        Args:
            args 命令行参数
            
        Returns:
                      返回网页中的所有链接. 
        """
        try:
            file_object = open(self.save_path + "/" + self._converse_url_to_filename(url_name), 'w')
            file_object.write(all_the_text)
            file_object.close()
        except IOError:
            print "write file ./urls failed."
  
    def _converse_url_to_filename(self, url_name):
        url_name = url_name.replace(":", "_")
        url_name = url_name.replace("/", "_")
        url_name = url_name.replace("\\", "_")
        url_name = url_name.replace(".", "_")
        if not url_name.endswith(".htm"):
            url_name = url_name + ".htm"  # 添加文件名后缀
        return url_name
    

 
prog = re.compile("(?<=href=\")[\\s\\S]+(?=\")") # 匹配连接正则表达式

