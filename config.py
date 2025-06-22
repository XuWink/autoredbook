from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


########## Selenium 配置 ##########
edge_options = Options()
# edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
service = Service(r"data/msedgedriver.exe")  # 替换为你的 chromedriver 路径
Browser = webdriver.Edge(service=service, options=edge_options)

########## 小红书 配置 ##########
phone = "12345678901"
title = ""  # 标题
describe = "晚上好~求关注"  # 描述

# 图片存放路径
FLODER_PATH = 'images'
PathImage = None

########## telegram 配置 ##########
api_id = '12313213'
api_hash = "a34dcfe5eafc3ee3e168b99aaaaaaaaa"
phone_number = "8612345678901"
channel_link = "https://t.me/SomeACG"
# proxy = (socks.SOCKS5, "0.0.0.0", 7897)  # 不需要代理则删除此行及socks导入
picture_storage_path = "images/"