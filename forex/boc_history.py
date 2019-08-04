#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/3/2019 1:26 PM
# @Author  : HowsonLiu
# @File    : boc_history.py
import json
import os
import datetime

HISTORY_FILE_PATH = './forex/history.json'


class BOCFCStruct:
    """bank of china's foreign currency struct"""
    name = None
    spot_rate = None
    cash_offer = None

    def __str__(self):
        """serialization"""
        return '{0} {1} {2}'.format(self.name, self.spot_rate, self.cash_offer)

    @staticmethod
    def from_str(s):
        """deserialization"""
        arr = s.split()
        struct = BOCFCStruct()
        struct.name = arr[0]
        struct.spot_rate = arr[1]
        struct.cash_offer = arr[2]
        return struct


class BOCHistory:
    @staticmethod
    def read_history():
        """
        read the dict from file
        :return: a dict liked {"date": str(the BOCFCStructs' list)}
        """
        if os.path.exists(HISTORY_FILE_PATH):
            with open(HISTORY_FILE_PATH) as file:
                return json.load(file)
        return {}

    @staticmethod
    def save_history(history):
        """
        save the dict to file
        :param history: a dict liked {"date": [str(BOCFCStruct), str(BOCFCStruct)]}
        :return: None
        """
        with open(HISTORY_FILE_PATH, 'w') as file:
            json.dump(history, file)


class BOCHistoryHandler:
    history = {}

    def __init__(self):
        self.history = BOCHistory.read_history()

    def write_and_save_today(self, fc_list):
        """
        write today BOCFCStruct list on history file
        :param fc_list: a BOCFCStruct list from caller(spider)
        :return: None
        """
        time_str = datetime.datetime.now().strftime('%Y-%m-%d')
        fc_list_tmp = []
        for fc in fc_list:
            fc_list_tmp.append(str(fc))
        fc_list_str = ','.join(fc_list_tmp)     # list serialization
        self.history[time_str] = fc_list_str
        BOCHistory.save_history(self.history)

    def read_offset_day_fc(self, offset_day):
        """
        read previous day fc list
        :param offset_day: offset_day = -1 is yesterday, offset_day = 1 is tomorrow(never use)
        :return: a BOCFCStruct list
        """
        offset_day_str = (datetime.datetime.now() + datetime.timedelta(days=offset_day)).strftime('%Y-%m-%d')
        offset_day_fc_list = []
        try:
            offset_day_fc_list_str = self.history[offset_day_str]
            offset_day_fc_list = offset_day_fc_list_str.split(',')
            for i in range(0, len(offset_day_fc_list)):     # list deserialization
                offset_day_fc_list[i] = BOCFCStruct.from_str(offset_day_fc_list[i])
        except:
            pass
        return offset_day_fc_list

