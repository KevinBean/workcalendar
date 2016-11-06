# -*- coding=utf-8 -*-
'''
1. 直接用python遍历硬盘文件名（自动）
2. 用python分析每月的词频（根据文件名）
2. 挑出每月的差异词
3. 建立日历
'''
import os
import time
import csv
import pandas as pd
import calendar
import jieba
def folderWalk(rootDir,filename):
    '''
    读取根目录下文件夹和文件夹信息，输出csv文件
    :param rootDir: 根目录
    :param filename: 输出csv文件名
    :return:
    '''
    list_dirs = os.walk(rootDir)
    csvfile = file(filename,'wb')
    writer = csv.writer(csvfile)
    title = ['Name','ModifiedTime','CreatedTime']
    writer.writerow(title)
    for root,dirs,files in list_dirs:
        for d in dirs:
            mtime = os.path.getmtime(os.path.join(root,d))
            ctime = os.path.getctime(os.path.join(root, d))
            dline = [d.encode('utf-8'),mtime,ctime]
            print dline
            writer.writerow(dline)
        for f in files:
            mtime = os.path.getmtime(os.path.join(root, f))
            ctime = os.path.getctime(os.path.join(root, f))
            fline = [f.encode('utf-8'), mtime, ctime]
            writer.writerow(fline)
    csvfile.close()
    return rootDir,filename

def word_frequency(text):
    '''
    利用jieba计算词频
    :param text:
    :return:
    '''
    print text
    from collections import Counter
    words = [word for word in jieba.cut(text) if len(word) >= 2]
    c = Counter(words)
    print words
    for word_freq in c.most_common(20):
        word, freq = word_freq
        print word, freq

def cat_by_created(filename):
    '''
    按月份归类统计，其中年份取2000-2020
    :param filename:
    :return:
    '''
    data = pd.read_csv(filename)
    for month in range(1,13):
        data_for_month = pd.Series()
        for year in range(2000,2020):
            startDay,stopDay = calendar.monthrange(year,month) # 用calendar获取每月起始日起
            startTime = time.mktime((year,month,startDay,0,0,0,0,0,0)) #每月开始时间戳
            stopTime = time.mktime((year,month,stopDay,0,0,0,0,0,0)) #每月结束时间戳
            # print data['CreatedTime'],startTime
            data_for_year = data[data[u'CreatedTime'] >= startTime] # 筛选当月数据
            # print data_for_year
            data_for_year = data_for_year[data_for_year[u'CreatedTime'] <= stopTime] # 筛选当月数据
            # print data_for_year
            data_for_month = pd.concat([data_for_month,data_for_year]) # 保存当年的当月数据
        data_for_month[u'Name'].to_csv('month'+str(month)+filename,index=False) # 保存每年的当月数据

if __name__ =='__main__':
    # rootDir = '/Users/bianbin/PycharmProjects/chatbot' # for mac
    rootDir =u'D:\\工程\\' # for windows
    filename = 'file.csv'
    folderWalk(rootDir,filename)
    cat_by_created(filename)
    for month in range(1, 13):
        filename_by_month = 'month' + str(month) + filename
        csvfile = file(filename_by_month,'rb')
        reader = csv.reader(csvfile)
        nametext = csvfile.read() # 第四列是文件名列
        # print  str(nametext)
        word_frequency(nametext.decode('utf-8'))

