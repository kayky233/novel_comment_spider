# -*- coding: UTF-8 -*-
import pandas as pd
from datetime import datetime, timedelta

import locale
locale.setlocale(locale.LC_CTYPE,'chinese')

# 创建示例数据
allItemsPD =  pd.read_csv("wuxia.csv",encoding='utf_8_sig')

# 将时间格式转换为年月格式
def convert_date(date_str):
    now = datetime.now()
    if 'years ago' in date_str:
        years_ago = int(date_str.split('years ago')[0])
        date = now - timedelta(days=years_ago*365)
    elif 'months ago' in date_str:
        months_ago = int(date_str.split('months ago')[0])
        date = now - timedelta(days=months_ago*30)
    elif 'year ago' in date_str:
        year_ago = int(date_str.split('year ago')[0])
        date = now - timedelta(days=year_ago*365)
    elif 'month ago' in date_str:
        month_ago = int(date_str.split('month ago')[0])
        date = now - timedelta(days=month_ago*30)
    elif 'days ago' in date_str:
        days_ago = int(date_str.split('days ago')[0])
        date = now - timedelta(days=days_ago * 1)
    elif 'day ago' in date_str:
        day_ago = int(date_str.split('day ago')[0])
        date = now - timedelta(days=day_ago * 1)
    else:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime('%Y年%m月')
allItemsPD['ReviewTime'] = allItemsPD['ReviewTime'].apply(convert_date)
print(allItemsPD['ReviewTime'])
allItemsPD.to_csv("wuxia.csv",encoding='utf_8_sig')