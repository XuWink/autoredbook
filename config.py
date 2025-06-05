from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# 配置 EdgeDriver
edge_options = Options()
# edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
service = Service(r'D:/xuwenke/study_python3/tt/asserts/edgedriver_win64/msedgedriver.exe')  # 替换为你的 chromedriver 路径

# 启动浏览器
Browser = webdriver.Edge(service=service, options=edge_options)


# 当前登录用户
CurrentUser = None

# 实例
# Browser = None

# 小红书登录的手机号
phone = "17591236011"
# 标题，描述
title = "自动化发布小红书笔记"
describe = "测试自动化发布小红书笔记"

# 图片存放路径
PathImage = r"C:\Users\wenke.xu\Pictures\Saved Pictures\20200817233333_ofpwg.jpg"