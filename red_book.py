import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import config as Config
import pickle


def login():
    Config.Browser.get("https://creator.xiaohongshu.com/login")

    # 加载 Cookie（如果存在）
    try:
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            Config.Browser.add_cookie(cookie)
        Config.Browser.refresh()  # 刷新页面以应用 Cookie
        print("Cookies loaded and applied.")
    except FileNotFoundError:
        print("No cookies file found. Proceeding with fresh login.")

    # 显式等待登录页面加载
    WebDriverWait(Config.Browser, 10).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "input[placeholder='手机号']")
    )
    # 输入手机号
    phone_input = Config.Browser.find_element(By.CSS_SELECTOR, "input[placeholder='手机号']")
    phone_input.send_keys(Config.phone)
    phone_input.send_keys(Keys.TAB)
    time.sleep(1)  # 短暂等待

    # 点击获取验证码按钮（假设类名是稳定的）
    verify_btn = WebDriverWait(Config.Browser, 10).until(
        lambda d: d.find_element(By.XPATH, "//*[@id='page']/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]")
    )
    verify_btn.click()

    
    # 输入验证码
    verify_code = input("请输入验证码: ")
    while len(verify_code) != 6:
        verify_code = input("验证码必须是6位数字，请重新输入: ")
    time.sleep(3)

    # 找到验证码输入框并输入
    verify_input = WebDriverWait(Config.Browser, 10).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "input[placeholder='验证码']")
    )
    verify_input.send_keys(verify_code)
    time.sleep(3)

    # 点击登录按钮
    login_button = WebDriverWait(Config.Browser, 10).until(
        lambda d: d.find_element(By.XPATH, "//*[@id='page']/div/div[2]/div[1]/div[2]/div/div/div/div/div/button")
    )
    login_button.click()
    time.sleep(50)

    print("success login")
    with open("cookies.pkl", "wb") as file:
        pickle.dump(Config.Browser.get_cookies(), file)
    time.sleep(3)

def uploadNote():
    if Config.Browser.current_url != "https://creator.xiaohongshu.com/publish/publish":
        Config.Browser.get("https://creator.xiaohongshu.com/publish/publish")
    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "div.tab:nth-child(2)")).click()
    except TimeoutException:
        print("网页好像加载失败了！请重试！")
    #  上传图片
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-wrapper > div:nth-child(1) > input:nth-child(1)").send_keys(
        Config.PathImage)
    Config.Browser.find_element(By.CSS_SELECTOR, ".el-input__inner").send_keys(Config.title)
    Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea").send_keys(Config.describe)
    print("等待资源上传……")
    time.sleep(10)
    create_js = f'return document.querySelector(".publishBtn")'
    Config.Browser.execute_script(create_js).click()
    print("发布成功！")
    print("等待页面返回！")
    time.sleep(5)
    Config.Browser.quit()

def init():
    # 谷歌浏览器
    # Config.Browser = webdriver.Chrome()
    # Config.PathImage = f'C:\\Users\\I584846\\Downloads\\a.jpg'
    # Config.title = "我的第一个笔记"
    # Config.describe = "我的第一个笔记"
    pass


def start():
    try:
        # 初始化
        init()
        #   登录
        login()
        # 上传笔记
        # uploadNote()
    except KeyboardInterrupt:
        print("\nBye!")
    except Exception as e:
        print(f"发生了一些错误：\n{e}")