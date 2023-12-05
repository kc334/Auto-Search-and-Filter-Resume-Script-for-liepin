import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

brower = webdriver.Chrome()
wait = WebDriverWait(brower, 10)

url = "https://rd6.zhaopin.com"
brower.get(url)
bcookies  = brower.get_cookies()

# 登录前的cookie  输出登录前的cookie
cookies_nologin = {}
for item in bcookies:
    cookies_nologin[item['name']] = item['value']
print(cookies_nologin)
print("\n\n")

# 60s内手动完成qq音乐网页登录的一系列操作
# 包括点击登录---点击密码登录---输入账号密码--点击登录  最终完成登录  
# 记录登录后的cookies信息存储在 当前代码路径下的   cookie.pickle文件中
time.sleep(15)  

# 得到登录后的cookies信息
bcookies  = brower.get_cookies()

# 登录后的cookie  输出登录后的cookie 
cookies = {}
for item in bcookies:
    cookies[item['name']] = item['value']
    outputPath = open('cookie.pickle','wb')
    pickle.dump(cookies,outputPath)
#print(browser.get_cookies())
print(cookies)
print("\n\n")
