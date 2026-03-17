"""
Playwright 版本的 FARFETCH 爬虫配置
自动生成于: setup_config.py
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
PAGE_LOAD_WAIT = (6000, 7000)  # 6000-7000秒

# 滚动次数和间隔
SCROLL_COUNT = (5, 8)  # 5-8次滚动
SCROLL_INTERVAL = 1000  # 每次滚动间隔 1 秒

# 页面间延时
BETWEEN_PAGES = (7000, 8000)  # 7-8秒

# 任务间延时
BETWEEN_TASKS = (7000, 8000)  # 7-8秒

# 任务间短延时（只是跳过文件时）
BETWEEN_TASKS_SHORT = 1000  # 1秒

# ==================== 浏览器配置 ====================
HEADLESS = False  # 是否无头模式
SLOW_MO = 0  # 慢动作模式（毫秒），用于调试
TIMEOUT = 120000  # 默认超时时间（毫秒）- 120秒

# ==================== 超时时间测试配置 ====================
# 可以在这里修改超时时间进行测试
# 推荐值：60000(60秒), 90000(90秒), 120000(120秒), 180000(180秒)
# 测试方法：修改下面的值，然后运行测试
# 建议：从较小的值开始，如果超时则逐步增加

# 测试配置（用于测试不同超时时间）
# 运行: python3 -m playwright_crawler.batch_crawler data/女鞋类目_测试3条.csv
# 观察日志中的 "页面加载耗时"，选择合适的超时时间

# 测试模式：设置为 True 时启用测试模式
TEST_MODE = False  # 是否启用测试模式

# 测试超时时间（仅在 TEST_MODE=True 时生效）
TEST_TIMEOUT = 120000  # 测试用超时时间（毫秒）
