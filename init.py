#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/25/2019 8:38 PM
# @Author  : HowsonLiu
# @File    : init.py

from global_variable import CONFIG_PATH
import os.path

CONFIG_STR = '''
[email_sender]
server_address=
server_port=
account=
password=
display_name=
 
[forex_recv_email_account]
recv_email_account1=
; recv_email_account2=
; recv_email_account3=
; add account like that 
'''


def check_and_create_configure_file():
    if not os.path.exists(CONFIG_PATH):
        cfg_file = open(CONFIG_PATH, 'w', encoding='utf-8')
        cfg_file.write(CONFIG_STR)
        cfg_file.close()


check_and_create_configure_file()
