from telethon import TelegramClient, sync
import os
import socks
from telethon.tl.types import InputMessagesFilterPhotos
from datetime import datetime, timezone

from config import api_id, api_hash, picture_storage_path, phone_number, channel_link

def downloader_images_from_telegram():
    # 获取今天 0 点，带上 UTC 时区信息
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    client = TelegramClient('my_session', api_id=api_id, api_hash=api_hash).start(phone=phone_number)

    # 遍历频道图片消息（按时间倒序，最新优先）
    photos = client.get_messages(
        channel_link,
        limit=20,  # 无限制获取所有消息
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
