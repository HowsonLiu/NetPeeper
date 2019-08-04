#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/27/2019 3:38 PM
# @Author  : HowsonLiu
# @File    : run.py

import myemail.email_sender
import forex.boc_spider

emailsender=myemail.email_sender.EmailSender()
emailsender.init_sender()
emailsender.init_forex()
spider = forex.boc_spider.BOCSpider()
spider.get_fc_detail()
spider.boc_history_handler.write_and_save_today(spider.today_fc_detail_list)
emailsender.send_forex('Today Forex', spider.fill_html())

