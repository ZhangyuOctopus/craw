import concurrent.futures
import re
import time

import openpyxl as op
import pandas as pd
from bs4 import BeautifulSoup
import web_spider


def write_to_excel(data):
    wb = op.Workbook()
    ws = wb['Sheet']
    ws.append(['序号', '标题', '日期', '阅读量'])
    dfData = {
        '序号': data[0],
        '标题': data[1],
        '日期': data[2],
        '阅读量': data[3]
    }
    # 创建DataFrame
    df = pd.DataFrame(dfData)
    # 存表，去除原始索引列（0,1,2...）
    df.to_excel('multi-threadr.xlsx', index=False)


def craw():
    with concurrent.futures.ThreadPoolExecutor() as pool:
        htmls = pool.map(web_spider.craw, web_spider.urls)
        title, date, read = list(), list(), list()
        for content in htmls:
            soup = BeautifulSoup(content, 'html.parser')
            rows = soup.find_all(attrs={'class': '_3HG1uUQ3C2HBEsGwDWY-zw'})
            for row in rows:
                # 标题
                _title = row.find(attrs={'class': '_3_JaaUmGUCjKZIdiLhqtfr'})
                title.append(_title.get_text())

                _date = row.find(attrs={'class': '_3TzAhzBA-XQQruZs-bwWjE'})
                d = str(_date)
                res = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", d)
                date.append(res.group())

                # 阅读量
                _read = row.find(attrs={'class': '_2gvAnxa4Xc7IT14d5w8MI1'})
                read.append(_read.get_text())
        nums = [i for i in range(1, len(title) + 1)]
        data = [nums, title, date, read]
        write_to_excel(data)


if __name__ == '__main__':
    start = time.time()
    craw()
    end = time.time()
    print("多线程耗时:", end - start)