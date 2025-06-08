'''
每日一言
'''
import os
import random
import requests

def fetch_hitokoto() -> str:
    """
    获取一言网站的句子
    
    Returns:
        成功时返回一言文本，失败时返回错误信息
    """
    try:
        # 发送HTTP请求
        response = requests.get('https://v1.hitokoto.cn/?c=f&encode=text')
        
        # 检查响应状态
        response.raise_for_status()  # 状态码非200时抛出异常
        
        # 提取并返回文本
        return response.text.strip()
        
    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {e}"
    except Exception as e:
        return f"发生未知错误: {e}"
    

def load_random_image(folder_path='images'):
    """
    从指定文件夹随机加载一张图片
    
    Args:
        folder_path: 图片文件夹路径，默认为'images'
    
    Returns:
        PIL.Image对象或None（如果未找到图片）
    """
    # 支持的图片文件扩展名
    IMAGE_EXTENSIONS = [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
        '.webp', '.tiff', '.svg', '.ico'
    ]
    
    try:
        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            print(f"错误：文件夹 '{folder_path}' 不存在")
            return None
            
        # 获取所有图片文件
        image_files = [
            f for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
            and os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
        ]
        
        # 检查是否有图片文件
        if not image_files:
            print(f"错误：文件夹 '{folder_path}' 中未找到图片")
            return None
            
        # 随机选择一张图片
        random_image = random.choice(image_files)
        image_path = os.path.join(folder_path, random_image)
        
        # 返回图片路径
        return image_path
        
    except Exception as e:
        print(f"加载图片时出错: {e}")
        return None
    

def delete_image(image_path):
    """
    删除指定路径的图片文件
    
    Args:
        image_path: 图片文件的完整路径（例如：./images/test.jpg）
    
    Returns:
        bool: 删除成功返回 True，失败返回 False
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"错误：文件 '{image_path}' 不存在")
            return False
            
        # 检查是否为文件（非文件夹）
        if not os.path.isfile(image_path):
            print(f"错误：'{image_path}' 不是文件")
            return False
            
        # 删除文件
        os.remove(image_path)
        print(f"成功删除文件：{image_path}")
        return True
        
    except Exception as e:
        print(f"删除文件时出错：{e}")
        return False
    

# 获取当前工作目录
# current_dir = os.getcwd()
# 构建完整路径
# image_folder = "images"
# filename = "微信图片_20250608184419_10.jpg"