#! /usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import datetime
import time


# 随机字符串
def random_str():
    return str(uuid.uuid1()).replace('-', '')[:20]


# datetime -> timestamp
def datetime2timestamp(date):
    return time.mktime(date.timetuple())


# timestamp -> datetime
def timestamp2datetime(date):
    return datetime.datetime.fromtimestamp(float(date))


# 获取今日0点的时间
def get_today_start():
    today = datetime.datetime.today()
    todayemp = today
    today_start = todayemp.replace(hour=0, minute=0, second=0, microsecond=0)
    return today_start


# 获取今日24点的时间
def get_today():
    today = datetime.datetime.today()
    tomorrowemp = today + datetime.timedelta(days=1)
    tomorrow = tomorrowemp.replace(hour=0, minute=0, second=0, microsecond=0)
    return tomorrow


# 获取明日24点的时间
def get_tomorrow():
    today = datetime.datetime.today()
    tomorrowemp = today + datetime.timedelta(days=2)
    tomorrow = tomorrowemp.replace(hour=0, minute=0, second=0, microsecond=0)
    return tomorrow


# 获取本周末24点的时间
def get_week():
    today = datetime.datetime.today()
    tomorrowemp = today + datetime.timedelta(days=7 - today.weekday())
    week = tomorrowemp.replace(hour=0, minute=0, second=0, microsecond=0)
    return week


# 获取本周末24点的时间
def get_month():
    today = datetime.datetime.today()
    tomorrowemp = today + datetime.timedelta(days=30 - today.day)
    month = tomorrowemp.replace(hour=0, minute=0, second=0, microsecond=0)
    return month
