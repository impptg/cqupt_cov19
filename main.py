# -*- coding: utf-8 -*-
# create by pptg 2020-08-14 #
import time
import numpy as np
from selenium import webdriver
from collections import Counter
import os
import pandas as pd
import datetime

def getval(str):
    d = int(str[21:23])
    h = int(str[24:26])
    m = int(str[27:29])
    return m + h*60 + d*24*60

# args
d = datetime.date.today().strftime('%Y-%m-%d')
url_log = 'https://ids.cqupt.edu.cn/authserver/login?service=http%3A%2F%2F172.20.2.47%2Fstudp%2Fpanel%2Fidslogin.php'
url_data = 'http://172.20.2.47/studp/XiaoLingDao/studentXiaoLingDaoBKSMeiRiDaKaLiShi2.php?excel=1&s1011=%E8%AF%B7%E8%BE%93%E5%85%A5%E5%AD%A6%E5%8F%B7&s1012=%E8%AF%B7%E8%BE%93%E5%85%A5%E5%A7%93%E5%90%8D&s1013=%E5%85%A8%E9%83%A8%E5%AD%A6%E9%99%A2&s1014=%E5%85%A8%E9%83%A8%E5%B9%B4%E7%BA%A7&s1015=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%8F%AD%E7%BA%A7%E5%8F%B7&s1016=%E9%92%9F%E6%A5%A0&s1017='+d

# get data
driver = webdriver.Chrome()
driver.get(url_log)
driver.find_element_by_id("username").send_keys("0101399")
driver.find_element_by_id("password").send_keys("xiaonan574018")
driver.find_element_by_class_name('img1').click()
driver.get(url_data)
time.sleep(3)
driver.quit()

# choose the lastest file
t_file = ''
t_v = 0
files = '/Users/pptg/Downloads/'
for filename in os.listdir(files):
    if filename[0:2] == '打卡':
        v = getval(filename)
        if v > t_v:
            t_file = filename
            tv = v

# read file sort by id
data = pd.read_csv(files + t_file,encoding='gbk',delimiter=',')
data = np.array(data)
data = data[data[:,5].argsort()]

# who doesn't finish it
nodata = data[data[:,7]=='否\t',:]

# data's information
c_data = Counter(nodata[:,5])
n = nodata.shape[0]
m = nodata.shape[1]

# print result
print(t_file)
for i in c_data:
    print(str(i)+'班 '+str(c_data[i])+' 人未打卡')
    for j in range(n):
        if(nodata[j,5] == i):
            print(str(nodata[j, 5]) + ' ' + str(nodata[j, 2])
                  + str(nodata[j, 7]))
    print('')