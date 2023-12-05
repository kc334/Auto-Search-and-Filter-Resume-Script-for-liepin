# 智联招聘AI搜索筛选脚本
## Approach
使用selenium模拟点击实现爬取简历内容，用openai gpt api判断简历内容是否符合职位要求
## Usage
### 1.先在搜索界面把常用的初步筛选条件保存为快捷搜索（年龄，院校等）
### 2.运行login.py，登录账户
### 3.测试selenium
运行test_webDriver.py，检查模拟操作和爬取逻辑是否运行正常
### 4.测试Openai api
先在项目根目录创建一个文件加apiKey.txt，在里面填入你的Openai key
然后运行test_gpt_api，测试发送和接收api是否正常和检查gpt筛选结果

### 5.hire.py包括3和4的整合，实现自动操作和自动筛选