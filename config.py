from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# 配置 EdgeDriver
edge_options = Options()
# edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
service = Service(r'data/msedgedriver.exe')  # 替换为你的 chromedriver 路径

# 启动浏览器
Browser = webdriver.Edge(service=service, options=edge_options)


# 当前登录用户
CurrentUser = None

# 实例
# Browser = None

# 小红书登录的手机号
phone = "17591236011"
# 标题，描述
title = ""
describe = "晚上好~求关注"

# 图片存放路径
FLODER_PATH = 'images'
PathImage = r"C:\\Users\\hp\\Pictures\\壁纸\\14.jpg"