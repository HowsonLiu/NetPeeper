#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/25/2019 8:36 PM
# @Author  : HowsonLiu
# @File    : email_sender.py

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import configparser
import sys
sys.path.append('..')
from NetPeeper.global_variable import CONFIG_PATH


class EmailSender:
    sender = None
    sender_address = None
    sender_port = None
    sender_account = None
    sender_password = None
    sender_name = None
    forex_recv_account = []

    def init_sender(self):
        conf = configparser.ConfigParser()
        conf.read(CONFIG_PATH, encoding='utf-8')
        self.sender_address = conf.get('email_sender', 'server_address')
        self.sender_port = conf.getint('email_sender', 'server_port')
        self.sender_account = conf.get('email_sender', 'account')
        self.sender_password = conf.get('email_sender', 'password')
        self.sender_name = conf.get('email_sender', 'display_name')

    def init_forex(self):
        conf = configparser.ConfigParser()
        conf.read(CONFIG_PATH, encoding='utf-8')
        for k, v in conf.items('forex_recv_email_account'):
            self.forex_recv_account.append(v)

    def send_forex(self, subject_text, html_text):
        self.sender = smtplib.SMTP_SSL(self.sender_address, self.sender_port)
        self.sender.login(self.sender_account, self.sender_password)
        print('Note: Login success!')
        msg = MIMEText(html_text, 'html', 'utf-8')
        msg['From'] = formataddr([self.sender_name, self.sender_account])
        msg['To'] = ', '.join(self.forex_recv_account)
        msg['Subject'] = subject_text
        self.sender.sendmail(self.sender_account, self.forex_recv_account, msg.as_string())
