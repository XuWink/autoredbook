from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

import config as Config
import pickle

from yiyan import fetch_hitokoto, load_random_image, delete_image


def login():
    # 打开登录页面
    Config.Browser.get("https://www.xiaohongshu.com/explore?language=zh-CN")
    sleep(5)
    
    # 加载已有Cookie（如果存在）
    try:
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        if cookies:  # 检查cookie文件是否非空
            for cookie in cookies:
                Config.Browser.add_cookie(cookie)
            Config.Browser.refresh()  # 刷新页面应用Cookie
            print("Cookies已加载并应用")
            # 验证是否成功登录（通过检测登录后才有的元素）
            try:
                WebDriverWait(Config.Browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".user"))  # 替换为实际登录后存在的元素选择器
                )
                print("基于Cookie的自动登录成功")
                return True  # 成功登录直接返回
            except TimeoutException:
                print("Cookie登录验证失败，继续常规登录流程")
        else:
            print("Cookie文件为空，继续常规登录流程")
    except FileNotFoundError:
        print("未找到Cookie文件，开始新登录流程")
    
    try:
        # 等待手机号输入框加载完成
        phone_input = WebDriverWait(Config.Browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='输入手机号']"))
        )
        phone_input.clear()  # 清空输入框
        phone_input.send_keys(Config.phone)
        sleep(5)
        
        # 点击获取验证码按钮
        phone_input.send_keys(Keys.TAB)
        verify_btn = WebDriverWait(Config.Browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div[1]/div/div[1]/div[3]/div[2]/form/label[2]/span"))  # 使用更稳定的XPath
        )
        verify_btn.click()
        print("已发送验证码，请查收")
        sleep(5)
        
        # 输入验证码（添加重试逻辑）
        max_attempts = 3
        for attempt in range(max_attempts):
            verify_code = input("请输入6位验证码: ").strip()
            if verify_code.isdigit() and len(verify_code) == 6:
                break
            else:
                print(f"无效验证码（尝试{attempt+1}/{max_attempts}）")
                if attempt == max_attempts - 1:
                    print("验证码输入尝试次数过多，退出登录流程")
                    return False
        
        # 输入验证码
        verify_input = WebDriverWait(Config.Browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='输入验证码']"))
        )
        verify_input.clear()
        verify_input.send_keys(verify_code)
        sleep(5)
        
        # 点击登录按钮
        login_button = WebDriverWait(Config.Browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div[1]/div/div[1]/div[3]/div[2]/form/button"))  # 使用更稳定的XPath
        )
        login_button.click()
        sleep(5)

        agree_but = WebDriverWait(Config.Browser, 10).until(
            lambda b: b.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[2]/div[2]/div[3]/div/div[1]")
        )
        agree_but.click()
        sleep(5)
        
        # 验证登录是否成功（等待登录后才有的元素出现）
        WebDriverWait(Config.Browser, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".user"))  # 替换为实际登录后存在的元素选择器
        )
        print("登录成功")
        sleep(5)
        
        # 保存Cookie
        with open("cookies.pkl", "wb") as file:
            pickle.dump(Config.Browser.get_cookies(), file)
        print("Cookie已保存")
        return True
        
    except TimeoutException as e:
        print(f"登录超时: {str(e)}")
        return False
    except WebDriverException as e:
        print(f"WebDriver操作异常: {str(e)}")
        return False
    except Exception as e:
        print(f"登录过程中发生未知错误: {str(e)}")
        return False


def uploadNote():
    if Config.Browser.current_url != "https://creator.xiaohongshu.com/publish/publish?source=official":
        Config.Browser.get("https://creator.xiaohongshu.com/publish/publish?source=official")

    try:
        # 点击 上传图文 标签
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.XPATH, "//*[@id='web']/div[1]/div/div/div[1]/div[3]")).click()
    except TimeoutException:
        print("网页好像加载失败了！请重试！")
    
    #  上传图片
    file_input = WebDriverWait(Config.Browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    file_input.send_keys(Config.PathImage)
    sleep(5)

    # 文章标题
    Config.Browser.find_element(By.XPATH, "//*[@id='web']/div[1]/div/div/div/div[1]/div[1]/div[4]/div[1]/div/input").send_keys(Config.title)
    sleep(3)

    # 描述
    Config.Browser.find_element(By.XPATH, "//*[@id='quillEditor']/div/p").send_keys(Config.describe)
    print("等待资源上传……")
    sleep(5)

    publishBtn = Config.Browser.find_element(By.XPATH, "//*[@id='web']/div[1]/div/div/div/div[2]/div/button[1]/div")
    publishBtn.click()
    print("发布成功！")
    sleep(5)
    Config.Browser.quit()

    # 删除图片
    delete_image(Config.PathImage)

def init():
    edge_options = Options()
    # edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    service = Service(r"data/msedgedriver.exe")  # 替换为你的 chromedriver 路径
    Config.Browser = webdriver.Edge(service=service, options=edge_options)

    # 获取当前工作目录
    import os
    current_dir = os.getcwd()

    # 构建完整路径
    Config.PathImage = load_random_image(os.path.join(current_dir, Config.FLODER_PATH))
    # Config.title = "我的第一个笔记"
    Config.describe = fetch_hitokoto()


def start():
    try:
        # 初始化
        init()
        # 登录
        login()
        # 上传笔记
        uploadNote()
    except KeyboardInterrupt:
        print("\nBye!")
    except Exception as e:
        print(f"发生了一些错误：\n{e}")