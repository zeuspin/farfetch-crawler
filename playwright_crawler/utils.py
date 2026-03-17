"""
工具函数模块
"""

import csv
import json
import re
import random
from pathlib import Path
from datetime import datetime
from .config import LOG_FILE, LOGS_DIR

# 确保日志目录存在
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def log(message):
    """记录日志到文件和控制台"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")


def parse_farfetch_product(text, href, img):
    """
    解析FARFETCH商品信息
    
    Args:
        text: 商品文本内容
        href: 商品链接
        img: 商品图片地址
        
    Returns:
        dict: 包含品牌、商品标题、价格、链接、图片的字典，或 None
    """
    text = text.strip()

    # 1. 提取品牌
    brand_match = re.match(r'(?:\d+%\s*优惠已计入)?\s*([A-Z][A-Za-z\s]+?)(?:[\u4e00-\u9fa5]|¥|可选尺码)', text)
    brand = brand_match.group(1).strip() if brand_match else ''

    # 如果没有品牌，尝试从href提取
    if not brand:
        brand_match = re.search(r'/shopping/women/([a-z0-9-]+)(?:--item|-item)', href)
        if brand_match:
            brand = brand_match.group(1).replace('-', ' ').upper()

    # 2. 提取价格
    prices = re.findall(r'¥[0-9,]+', text)
    price = ' '.join(prices) if prices else ''

    # 3. 提取标题
    title = ''
    if brand:
        text_without_brand = text.replace(brand, '', 1)
        text_without_discount = re.sub(r'^\d+%\s*优惠已计入', '', text_without_brand)

        if price:
            price_pos = text_without_discount.find(price[0])
            if price_pos > 0:
                title = text_without_discount[:price_pos].strip()
        else:
            title = re.sub(r'可选尺码：.*$', '', text_without_discount).strip()

    # 4. 处理链接
    full_link = href
    if href and not href.startswith('http'):
        full_link = 'https://www.farfetch.com' + href

    # 5. 处理图片
    full_image = img
    if img and not img.startswith('http'):
        full_image = 'https:' + img

    # 6. 清理标题
    title = re.sub(r'\s+', '', title)
    title = title.replace('优惠已计入', '').strip()

    if brand or title or price:
        return {
            '品牌': brand,
            '商品标题': title,
            '价格': price,
            '商品链接': full_link,
            '商品主图地址': full_image
        }
    return None


def load_tasks(csv_path):
    """
    加载任务 CSV 文件
    
    Args:
        csv_path: CSV 文件路径
        
    Returns:
        list: 任务列表
    """
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_products(products, csv_path):
    """
    保存商品数据到 CSV 文件
    
    Args:
        products: 商品列表
        csv_path: 输出 CSV 文件路径
    """
    fieldnames = ["品牌", "商品标题", "价格", "商品链接", "商品主图地址"]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)


def sanitize_filename(name):
    """
    清理文件名，替换特殊字符
    
    Args:
        name: 原始名称
        
    Returns:
        str: 清理后的名称
    """
    return name.replace('/', '-').replace('\\', '-').replace(':', '-')


def get_random_delay(min_max):
    """
    获取随机延时
    
    Args:
        min_max: (min, max) 元组，单位毫秒
        
    Returns:
        int: 随机延时值
    """
    return random.randint(min_max[0], min_max[1])
