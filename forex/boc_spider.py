#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/27/2019 1:30 PM
# @Author  : HowsonLiu
# @File    : boc_spider.py
from bs4 import BeautifulSoup
import sys
sys.path.append('..')
from NetPeeper.myhttp.myhttp import MyHttp
from NetPeeper.forex.boc_history import *

HTML_PATH = './forex/template.html'


class BOCSpider:
    """the spider of bank of china"""
    myhttp = MyHttp()
    boc_history_handler = BOCHistoryHandler()
    monitor_fc_type_list = ['日元', '港币', '美元']
    today_fc_detail_list = []
    yesterday_fc_detail_list = boc_history_handler.read_offset_day_fc(-1)
    seven_fc_detail_list = boc_history_handler.read_offset_day_fc(-7)

    def get_page_url(self, page):
        if page <= 0:
            return 'http://www.boc.cn/sourcedb/whpj/index.html'
        else:
            return 'http://www.boc.cn/sourcedb/whpj/index_{0}.html'.format(page)

    def get_fc_detail(self):
        cur_foreign_currency = self.monitor_fc_type_list
        cur_page_num = 0
        while len(cur_foreign_currency) > 0 and cur_page_num < 10:
            html = self.myhttp.get(self.get_page_url(cur_page_num))
            html.encoding = 'utf-8'
            cur_page_num += 1
            if html is None:
                continue
            soup = BeautifulSoup(html.text, 'lxml')
            foreign_currency_list = soup.find_all('tr')
            for c in foreign_currency_list:
                currency = c.find_all('td')
                if len(currency) > 0 and currency[0].text in cur_foreign_currency:
                    cur_foreign_currency.remove(currency[0].text)
                    fc = BOCFCStruct()
                    fc.name = currency[0].text
                    fc.spot_rate = currency[3].text
                    fc.cash_offer = currency[4].text
                    self.today_fc_detail_list.append(fc)

    def fill_html(self):
        html_file = open(HTML_PATH, 'r', encoding='utf-8')
        html_text = html_file.read()
        insert_text = ''
        line = '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>'
        for fc in self.today_fc_detail_list:
            insert_text += line.format(fc.name, fc.spot_rate, fc.cash_offer,
                                       self.calculate_yesterday(fc.name), self.calculate_seven(fc.name))
        return html_text.format(insert_text)

    def calculate_yesterday(self, fc_name):
        """
        compare fc_name today price to yesterday
        :param fc_name: forrign currency name
        :return: str which will show
        """
        prev_price = None
        cur_price = None
        for prev_fc in self.yesterday_fc_detail_list:
            if prev_fc.name == fc_name:
                prev_price = prev_fc.cash_offer
                break
        for cur_fc in self.today_fc_detail_list:
            if cur_fc.name == fc_name:
                cur_price = cur_fc.cash_offer
                break
        if prev_price is not None and cur_price is not None:
            rate = (float(cur_price) - float(prev_price)) / float(prev_price)
            if rate > 0:
                # return '↑ ' + '%.4f%%' % abs(rate)
                return '↑ ' + str(abs(rate))
            elif rate == 0:
                return 'same'
            else:
                # return '↓ ' + '%.4f%%' % abs(rate)
                return '↓ ' + str(abs(rate))
        else:
            return 'none'

    def calculate_seven(self, fc_name):
        """
        compare fc_name today price to seven day ago
        :param fc_name: forrign currency name
        :return: str which will show
        """
        prev_price = None
        cur_price = None
        for prev_fc in self.seven_fc_detail_list:
            if prev_fc.name == fc_name:
                prev_price = prev_fc.cash_offer
                break
        for cur_fc in self.today_fc_detail_list:
            if cur_fc.name == fc_name:
                cur_price = cur_fc.cash_offer
                break
        if prev_price is not None and cur_price is not None:
            rate = (float(cur_price) - float(prev_price)) / float(prev_price)
            if rate > 0:
                # return '↑ ' + '%.4f%%' % abs(rate)
                return '↑ ' + str(abs(rate))
            elif rate == 0:
                return 'same'
            else:
                # return '↓ ' + '%.4f%%' % abs(rate)
                return '↓ ' + str(abs(rate))
        else:
            return 'none'
