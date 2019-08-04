#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/27/2019 4:05 PM
# @Author  : HowsonLiu
# @File    : myhttp.py

import requests


class MyHttp:
    retry_time = 3
    se = requests.session()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/'
                  'signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '73.0.3683.86 Safari/537.36',
        'referer': '',
    }

    def get_html_response(self, url):
        """ my http get interface """
        try:
            res = self.se.get(url, headers=self.headers)
            if res.status_code != 200:
                print('Error: The get status code of ' + url + ' is ' + str(res.status_code))
                return None
        except Exception:
            print('Error: GET ' + url)
            return None
        return res

    def post_data(self, url, data):
        """ my http post interface"""
        try:
            res = self.se.post(url, data=data, headers=self.headers)
            if res.status_code != 200:
                print('Error: The post status code of ' + url + ' is ' + str(res.status_code))
                return None
        except:
            print('Error: POST ' + url)
            return None
        return res

    def get(self, url):
        cur_time = 0
        res = self.get_html_response(url)
        while res is None and cur_time < self.retry_time:
            res = self.get_html_response(url)
            cur_time += 1
        return res

    def post(self, url, data):
        cur_time = 0
        res = self.post_data(url, data)
        while res is None and cur_time < self.retry_time:
            res = self.post_data(url, data)
            cur_time += 1
        return res
