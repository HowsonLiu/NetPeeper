#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/27/2019 3:38 PM
# @Author  : HowsonLiu
# @File    : run.py

import myemail.email_sender
import forex.boc_spider
import schedule
import time

def forex_run():
    global emailsender
    try:
        spider = forex.boc_spider.BOCSpider()
        spider.get_fc_detail()
        spider.boc_history_handler.write_and_save_today(spider.today_fc_detail_list)
        emailsender.send_forex('Today Forex', spider.fill_html())
    except Exception as e:
        emailsender.send_forex('Error', repr(e))


emailsender = myemail.email_sender.EmailSender()
emailsender.init_sender()
emailsender.init_forex()
forex_run()
schedule.every().day.at('08:00').do(forex_run)
while True:
    schedule.run_pending()
    time.sleep(1)
