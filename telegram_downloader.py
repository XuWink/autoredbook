from telethon import TelegramClient, sync
import os
import socks
from telethon.tl.types import InputMessagesFilterPhotos
from datetime import datetime, timedelta

# =============需要被替换的值=================
api_id = '80xxxxx'
api_hash = "3066c1322d6931a85470xxxxxx"
channel_link = "https://t.me/SomeACG"
# proxy = (socks.SOCKS5, "0.0.0.0", 1080)  # 不需要代理则删除此行及socks导入
picture_storage_path = "images/"
# ==========================================

# 获取当天零点时间戳（UTC时间，需根据频道时区调整）
today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

client = TelegramClient('my_session', api_id=api_id, api_hash=api_hash).start()

# 遍历频道图片消息（按时间倒序，最新优先）
photos = client.get_messages(
    channel_link,
    limit=None,  # 无限制获取所有消息
    filter=InputMessagesFilterPhotos,
    reverse=False  # False=从新到旧，True=从旧到新
)

total = 0
downloaded = 0
for photo in photos:
    # 检查消息日期是否在当天（UTC时间，若频道用其他时区需调整时差）
    if photo.date >= today:
        total += 1
        filename = f"{picture_storage_path}/{photo.id}.jpg"
        print(f"检测到当天图片 ({total}): {filename}")
        if not os.path.exists(filename):
            client.download_media(photo, filename)
            print(f"下载完成: {filename}")
            downloaded += 1
        else:
            print(f"文件已存在: {filename}")

print(f"\n完成！共找到{total}张当天图片，成功下载{downloaded}张。")
client.disconnect()