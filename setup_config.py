#!/usr/bin/env python3
"""
配置引导工具
根据使用场景智能推荐配置参数
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title):
    """打印小节标题"""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}\n")


def get_choice(prompt, options, allow_custom=False):
    """
    获取用户选择
    
    Args:
        prompt: 提示信息
        options: 选项列表
        allow_custom: 是否允许自定义输入
        
    Returns:
        用户选择的值
    """
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    if allow_custom:
        print(f"  0. 自定义输入")
    
    while True:
        choice = input(f"\n{prompt} [1-{len(options)}" + (", 0" if allow_custom else "") + "]: ").strip()
        
        if allow_custom and choice == "0":
            custom = input("请输入自定义值: ").strip()
            return custom
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]
        except ValueError:
            pass
        
        print("⚠️ 无效选择，请重新输入")


def get_boolean_choice(prompt, default=True):
    """
    获取布尔选择
    
    Args:
        prompt: 提示信息
        default: 默认值
        
    Returns:
        bool: 用户选择
    """
    options = ["是", "否"]
    while True:
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            marker = " (默认)" if (i == 1 and default) or (i == 2 and not default) else ""
            print(f"  {i}. {option}{marker}")
        
        choice = input(f"\n请选择 [1-2]: ").strip()
        
        if choice == "1":
            return True
        elif choice == "2":
            return False
        elif choice == "":
            return default


def get_number_input(prompt, min_val, max_val, default):
    """获取数字输入"""
    while True:
        try:
            value = input(f"{prompt} [{min_val}-{max_val}] [默认: {default}]: ").strip()
            if not value:
                return default
            value = int(value)
            if min_val <= value <= max_val:
                return value
            print(f"⚠️ 请输入 {min_val}-{max_val} 之间的数字")
        except ValueError:
            print("⚠️ 请输入有效的数字")


def generate_config():
    """生成配置"""
    print_header("🎯 FARFETCH 爬虫配置引导")
    
    print("\n本工具将根据您的使用场景智能推荐配置参数。")
    print("所有配置都保存在 playwright_crawler/config.py 中。")
    
    # ========== 使用场景 ==========
    print_section("步骤 1/5: 选择使用场景")
    
    scenarios = {
        "快速测试": {
            "desc": "验证功能是否正常，爬取少量数据（1-2页）",
            "config": {
                "HEADLESS": False,
                "PAGE_LOAD_WAIT": (2000, 3000),
                "SCROLL_COUNT": (3, 5),
                "BETWEEN_PAGES": (2000, 3000),
                "BETWEEN_TASKS": (2000, 3000),
            }
        },
        "小规模爬取": {
            "desc": "爬取少量分类（10-20个），适合个人使用",
            "config": {
                "HEADLESS": False,
                "PAGE_LOAD_WAIT": (3000, 5000),
                "SCROLL_COUNT": (5, 8),
                "BETWEEN_PAGES": (5000, 10000),
                "BETWEEN_TASKS": (5000, 10000),
            }
        },
        "大规模爬取": {
            "desc": "爬取所有分类（88个），适合批量采集",
            "config": {
                "HEADLESS": True,
                "PAGE_LOAD_WAIT": (5000, 8000),
                "SCROLL_COUNT": (5, 8),
                "BETWEEN_PAGES": (10000, 15000),
                "BETWEEN_TASKS": (10000, 15000),
            }
        },
        "服务器运行": {
            "desc": "在无头服务器上长期运行",
            "config": {
                "HEADLESS": True,
                "PAGE_LOAD_WAIT": (8000, 12000),
                "SCROLL_COUNT": (5, 8),
                "BETWEEN_PAGES": (15000, 20000),
                "BETWEEN_TASKS": (15000, 20000),
            }
        },
    }
    
    scenario = get_choice("请选择使用场景", list(scenarios.keys()))
    config = scenarios[scenario]["config"].copy()
    
    print(f"\n✅ 已选择: {scenario}")
    print(f"   {scenarios[scenario]['desc']}")
    
    # ========== 无头模式 ==========
    print_section("步骤 2/5: 浏览器显示模式")
    
    print("无头模式不会显示浏览器窗口，适合服务器环境或后台运行。")
    print("有头模式可以看到浏览器操作过程，适合调试和验证。")
    
    headless = get_boolean_choice("是否启用无头模式？", config["HEADLESS"])
    config["HEADLESS"] = headless
    
    # ========== 网络环境 ==========
    print_section("步骤 3/5: 网络环境")
    
    print("网络环境会影响爬取速度和稳定性。")
    print("较慢的网络建议增加延时时间，避免请求失败。")
    
    network_options = ["高速网络（国内宽带/企业网络）", "普通网络（家庭宽带）", "较慢网络（海外/不稳定）"]
    network = get_choice("请选择网络环境", network_options)
    
    if "高速" in network:
        # 保持原配置或适当降低
        pass
    elif "普通" in network:
        # 增加延时
        config["PAGE_LOAD_WAIT"] = tuple(x + 2000 for x in config["PAGE_LOAD_WAIT"])
        config["BETWEEN_PAGES"] = tuple(x + 3000 for x in config["BETWEEN_PAGES"])
        config["BETWEEN_TASKS"] = tuple(x + 3000 for x in config["BETWEEN_TASKS"])
    else:
        # 大幅增加延时
        config["PAGE_LOAD_WAIT"] = tuple(x + 4000 for x in config["PAGE_LOAD_WAIT"])
        config["BETWEEN_PAGES"] = tuple(x + 5000 for x in config["BETWEEN_PAGES"])
        config["BETWEEN_TASKS"] = tuple(x + 5000 for x in config["BETWEEN_TASKS"])
    
    print(f"\n✅ 已选择: {network}")
    
    # ========== 懒加载配置 ==========
    print_section("步骤 4/5: 懒加载配置")
    
    print("懒加载通过滚动页面触发更多商品加载。")
    print("增加滚动次数可以加载更多商品，但会增加时间。")
    
    scroll_desc = {
        "保守（3-5次）": "快速，但可能遗漏部分商品",
        "平衡（5-8次）": "推荐，兼顾速度和完整性",
        "激进（8-12次）": "确保加载所有商品，但较慢",
    }
    
    scroll_choice = get_choice("滚动次数策略", list(scroll_desc.keys()))
    
    if "保守" in scroll_choice:
        config["SCROLL_COUNT"] = (3, 5)
    elif "平衡" in scroll_choice:
        config["SCROLL_COUNT"] = (5, 8)
    else:
        config["SCROLL_COUNT"] = (8, 12)
    
    print(f"\n✅ 已选择: {scroll_choice}")
    print(f"   {scroll_desc[scroll_choice]}")
    
    # ========== 自定义调整 ==========
    print_section("步骤 5/5: 自定义调整（可选）")
    
    custom = get_boolean_choice("是否需要自定义调整具体参数？", False)
    
    if custom:
        print("\n当前配置参数：")
        print(f"  页面加载等待: {tuple(config['PAGE_LOAD_WAIT'])}ms")
        print(f"  滚动次数: {tuple(config['SCROLL_COUNT'])}次")
        print(f"  页面间延时: {tuple(config['BETWEEN_PAGES'])}ms")
        print(f"  任务间延时: {tuple(config['BETWEEN_TASKS'])}ms")
        
        adjust_page = get_boolean_choice("是否调整页面加载等待？", False)
        if adjust_page:
            min_wait = get_number_input("最小等待时间", 1000, 20000, 3000)
            max_wait = get_number_input("最大等待时间", min_wait, 30000, 5000)
            config["PAGE_LOAD_WAIT"] = (min_wait, max_wait)
        
        adjust_scroll = get_boolean_choice("是否调整滚动次数？", False)
        if adjust_scroll:
            min_scroll = get_number_input("最少滚动次数", 1, 20, 5)
            max_scroll = get_number_input("最多滚动次数", min_scroll, 30, 8)
            config["SCROLL_COUNT"] = (min_scroll, max_scroll)
        
        adjust_between_pages = get_boolean_choice("是否调整页面间延时？", False)
        if adjust_between_pages:
            min_delay = get_number_input("最小延时", 1000, 30000, 5000)
            max_delay = get_number_input("最大延时", min_delay, 60000, 10000)
            config["BETWEEN_PAGES"] = (min_delay, max_delay)
        
        adjust_between_tasks = get_boolean_choice("是否调整任务间延时？", False)
        if adjust_between_tasks:
            min_delay = get_number_input("最小延时", 1000, 30000, 5000)
            max_delay = get_number_input("最大延时", min_delay, 60000, 10000)
            config["BETWEEN_TASKS"] = (min_delay, max_delay)
    
    # ========== 显示配置 ==========
    print_header("📋 配置建议")
    
    print(f"\n使用场景: {scenario}")
    print(f"无头模式: {'✅ 启用' if config['HEADLESS'] else '❌ 禁用'}")
    print(f"网络环境: {network}")
    print(f"\n详细配置:")
    print(f"  HEADLESS           = {config['HEADLESS']}")
    print(f"  PAGE_LOAD_WAIT     = {tuple(config['PAGE_LOAD_WAIT'])}  # 页面加载后等待时间（毫秒）")
    print(f"  SCROLL_COUNT       = {tuple(config['SCROLL_COUNT'])}  # 滚动次数")
    print(f"  SCROLL_INTERVAL    = 1000  # 每次滚动间隔（毫秒）")
    print(f"  BETWEEN_PAGES      = {tuple(config['BETWEEN_PAGES'])}  # 页面间延时（毫秒）")
    print(f"  BETWEEN_TASKS      = {tuple(config['BETWEEN_TASKS'])}  # 任务间延时（毫秒）")
    
    # ========== 应用配置 ==========
    print_section("应用配置")
    
    apply = get_boolean_choice("是否应用此配置？", True)
    
    if apply:
        config_file = project_root / "playwright_crawler" / "config.py"
        backup_file = config_file.with_suffix(".py.backup")
        
        # 备份原配置
        if config_file.exists():
            import shutil
            shutil.copy(config_file, backup_file)
            print(f"✅ 已备份原配置到: {backup_file}")
        
        # 写入新配置
        config_content = f'''"""
Playwright 版本的 FARFETCH 爬虫配置
自动生成于: {Path(__file__).name}
"""

from pathlib import Path

# ==================== 路径配置 ====================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# ==================== 输出配置 ====================
OUTPUT_BASE = OUTPUT_DIR

# ==================== 日志配置 ====================
LOG_FILE = LOGS_DIR / "playwright_crawler.log"

# ==================== 反爬延时配置（毫秒）====================
# 页面加载后等待时间
PAGE_LOAD_WAIT = {config['PAGE_LOAD_WAIT']}  # {config['PAGE_LOAD_WAIT'][0]}-{config['PAGE_LOAD_WAIT'][1]}秒

# 滚动次数和间隔
SCROLL_COUNT = {config['SCROLL_COUNT']}  # {config['SCROLL_COUNT'][0]}-{config['SCROLL_COUNT'][1]}次滚动
SCROLL_INTERVAL = 1000  # 每次滚动间隔 1 秒

# 页面间延时
BETWEEN_PAGES = {config['BETWEEN_PAGES']}  # {config['BETWEEN_PAGES'][0]//1000}-{config['BETWEEN_PAGES'][1]//1000}秒

# 任务间延时
BETWEEN_TASKS = {config['BETWEEN_TASKS']}  # {config['BETWEEN_TASKS'][0]//1000}-{config['BETWEEN_TASKS'][1]//1000}秒

# 任务间短延时（只是跳过文件时）
BETWEEN_TASKS_SHORT = 1000  # 1秒

# ==================== 浏览器配置 ====================
HEADLESS = {config['HEADLESS']}  # 是否无头模式
SLOW_MO = 0  # 慢动作模式（毫秒），用于调试
TIMEOUT = 60000  # 默认超时时间（毫秒）
'''
        
        config_file.write_text(config_content, encoding="utf-8")
        print(f"✅ 配置已保存到: {config_file}")
        
        print("\n" + "=" * 70)
        print("🎉 配置完成！")
        print("=" * 70)
        print("\n您现在可以使用以下命令开始爬取：")
        print("  python3 -m playwright_crawler.batch_crawler data/服装分类_示例.csv")
        print("\n或者使用交互式菜单：")
        print("  python3 quick_start.py")
        
    else:
        print("\n❌ 配置未应用，原配置保持不变。")
        print("   如需手动配置，请编辑: playwright_crawler/config.py")


def main():
    """主函数"""
    try:
        generate_config()
    except KeyboardInterrupt:
        print("\n\n⚠️ 配置已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 配置失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
