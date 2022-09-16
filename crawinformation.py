import re
import openpyxl as op
import pandas as pd
import requests
from bs4 import BeautifulSoup


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
    df.to_excel('result.xlsx', index=False)


def craw():
    # n为爬取的总页数
    n = 50
    # title存储标题, date存储日期, read存储阅读量
    title, date, read = list(), list(), list()
    for page in range(1, n + 1):
        # get函数发送get请求
        r = requests.get("https://www.aquanliang.com/blog/page/%d" % page)
        # r.text表示服务端返回的内容
        content = r.text
        # 使用BeautifulSoup解析html代码
        soup = BeautifulSoup(content, 'html.parser')
        # 使用使用BeautifulSoup解析html代码获取class属性等于_3HG1uUQ3C2HBEsGwDWY-zw的标签
        rows = soup.find_all(attrs={'class': '_3HG1uUQ3C2HBEsGwDWY-zw'})
        # 遍历当前这一页的内容
        for row in rows:
            # 标题
            _title = row.find(attrs={'class': '_3_JaaUmGUCjKZIdiLhqtfr'})
            title.append(_title.get_text())

            # 日期
            _date = row.find(attrs={'class': '_3TzAhzBA-XQQruZs-bwWjE'})
            d = str(_date)
            # 使用search方法匹配日期
            res = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", d)
            # group函数获取日期
            date.append(res.group())

            # 阅读量
            _read = row.find(attrs={'class': '_2gvAnxa4Xc7IT14d5w8MI1'})
            read.append(_read.get_text())
    # nums表示序号
    nums = [i for i in range(1, len(title) + 1)]
    data = [nums, title, date, read]
    # 写入到excel中
    write_to_excel(data)


if __name__ == '__main__':
    craw()