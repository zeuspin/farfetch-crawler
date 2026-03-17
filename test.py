#!/usr/bin/env python3
"""
验证脚本 - 测试项目是否可以正常运行
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_imports():
    """测试模块导入"""
    print("📦 测试模块导入...")
    try:
        import playwright_crawler
        from playwright_crawler import config, utils, batch_crawler, extract_categories
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False


def test_playwright():
    """测试 Playwright 是否安装"""
    print("\n🎭 测试 Playwright...")
    try:
        import playwright
        from playwright.sync_api import sync_playwright
        print("✅ Playwright 已安装")
        
        # 测试 Chromium 是否可用
        from playwright.sync_api import BrowserType
        print("✅ Chromium 浏览器可用")
        return True
    except ImportError:
        print("❌ Playwright 未安装")
        print("   请运行: pip3 install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Playwright 测试失败: {e}")
        return False


def test_data_files():
    """测试数据文件"""
    print("\n📊 测试数据文件...")
    
    example_csv = project_root / "data" / "服装分类_示例.csv"
    full_csv = project_root / "data" / "服装分类_完整版.csv"
    
    if example_csv.exists():
        print(f"✅ 示例文件存在: {example_csv}")
        line_count = len(example_csv.read_text().strip().split('\n'))
        print(f"   包含 {line_count} 行数据")
    else:
        print(f"❌ 示例文件不存在: {example_csv}")
        return False
    
    if full_csv.exists():
        print(f"✅ 完整文件存在: {full_csv}")
        line_count = len(full_csv.read_text().strip().split('\n'))
        print(f"   包含 {line_count} 行数据")
    else:
        print(f"❌ 完整文件不存在: {full_csv}")
        return False
    
    return True


def test_config():
    """测试配置"""
    print("\n⚙️ 测试配置...")
    from playwright_crawler.config import (
        OUTPUT_BASE, LOG_FILE,
        PAGE_LOAD_WAIT, HEADLESS
    )
    
    print(f"✅ 输出目录: {OUTPUT_BASE}")
    print(f"✅ 日志文件: {LOG_FILE}")
    print(f"✅ 页面加载等待: {PAGE_LOAD_WAIT}")
    print(f"✅ 无头模式: {HEADLESS}")
    
    return True


def test_utils():
    """测试工具函数"""
    print("\n🛠️ 测试工具函数...")
    from playwright_crawler.utils import (
        parse_farfetch_product,
        sanitize_filename,
        get_random_delay
    )
    
    # 测试商品解析
    result = parse_farfetch_product(
        "PRADA 女士连衣裙¥12,000",
        "/shopping/women/dress-1/item-123",
        "//image.jpg"
    )
    print(f"✅ 商品解析: {result}")
    
    # 测试文件名清理
    safe_name = sanitize_filename("测试/名称:2024")
    print(f"✅ 文件名清理: 测试/名称:2024 -> {safe_name}")
    
    # 测试随机延时
    delay = get_random_delay((3000, 5000))
    print(f"✅ 随机延时: {delay}ms")
    
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 FARFETCH 爬虫 - 验证测试")
    print("=" * 60)
    
    results = []
    
    results.append(test_imports())
    results.append(test_playwright())
    results.append(test_data_files())
    results.append(test_config())
    results.append(test_utils())
    
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有测试通过！项目可以正常运行。")
        print("\n📚 快速开始:")
        print("   python3 -m playwright_crawler.batch_crawler data/服装分类_示例.csv")
        return 0
    else:
        print(f"\n⚠️ 有 {total - passed} 个测试失败，请检查配置。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
