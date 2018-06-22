#! /usr/bin/env python
# -*- coding: utf-8 -*-

import utils

# 活动列表时间类型
TIME_TYPE_TODAY = '1'
TIME_TYPE_TOMORROW = '2'
TIME_TYPE_WEEKS = '3'
TIME_TYPE_MONTH = '4'


# 时间类型映射
LIMIT_TIME = {
    TIME_TYPE_TODAY: utils.get_today(),
    TIME_TYPE_TOMORROW: utils.get_tomorrow(),
    TIME_TYPE_WEEKS: utils.get_week(),
    TIME_TYPE_MONTH: utils.get_month()
}
