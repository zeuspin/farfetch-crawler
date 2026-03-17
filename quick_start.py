#!/usr/bin/env python3
"""
快速启动脚本
提供交互式菜单选择运行方式
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def check_dependencies():
    """检查依赖是否已安装"""
    try:
        import playwright
        return True
    except ImportError:
        return False


def install_dependencies():
    """安装依赖"""
    import subprocess
    
    print("\n📦 安装 Python 依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    print("\n📥 安装 Playwright 浏览器...")
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    
    print("\n✅ 依赖安装完成！")


def main():
    """主菜单"""
    print("=" * 60)
    print("🎉 FARFETCH 服装数据爬虫 - Playwright 版本")
    print("=" * 60)
    print()
    
    # 检查依赖
    if not check_dependencies():
        print("⚠️ 检测到未安装 Playwright")
        choice = input("是否立即安装依赖？(y/n): ")
        if choice.lower() == 'y':
            install_dependencies()
        else:
            print("❌ 请先安装依赖：pip install -r requirements.txt")
            print("   然后运行：playwright install chromium")
            sys.exit(1)
    
    print("\n📋 请选择运行方式：")
    print("  1. 快速测试（10个示例分类）")
    print("  2. 完整爬取（88个分类）")
    print("  3. 重新提取分类")
    print("  4. 自定义任务文件")
    print("  0. 退出")
    print()
    
    choice = input("请输入选项 (0-4): ").strip()
    
    if choice == "1":
        print("\n🚀 开始快速测试...")
        import asyncio
        from playwright_crawler.batch_crawler import run_batch
        asyncio.run(run_batch(str(project_root / "data" / "服装分类_示例.csv")))
    
    elif choice == "2":
        print("\n🚀 开始完整爬取...")
        import asyncio
        from playwright_crawler.batch_crawler import run_batch
        asyncio.run(run_batch(str(project_root / "data" / "服装分类_完整版.csv")))
    
    elif choice == "3":
        print("\n🚀 开始提取分类...")
        from playwright_crawler.extract_categories import main as extract_main
        extract_main()
    
    elif choice == "4":
        csv_path = input("\n请输入任务文件路径: ").strip()
        if not Path(csv_path).exists():
            print(f"❌ 文件不存在: {csv_path}")
            sys.exit(1)
        print(f"\n🚀 开始处理: {csv_path}")
        import asyncio
        from playwright_crawler.batch_crawler import run_batch
        asyncio.run(run_batch(csv_path))
    
    elif choice == "0":
        print("\n👋 再见！")
        sys.exit(0)
    
    else:
        print("\n❌ 无效选项")
        sys.exit(1)
    
    print("\n✅ 完成！")


if __name__ == "__main__":
    main()
