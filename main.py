from red_book import start
from telegram_downloader import downloader_images_from_telegram
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='选择操作：1-上传到小红书，2-从Telegram下载图片')
    
    # 添加参数 -n/--number，用于接收数字参数
    parser.add_argument('-n', '--number', type=int, required=True, help='操作编号')
    
    args = parser.parse_args()
    num = args.number
    
    if num == 1:
        # 自动化上传到小红书
        print("开始上传到小红书...")
        start()
    else:
        # 从telegram下载图片
        print("开始从Telegram下载图片...")
        downloader_images_from_telegram()