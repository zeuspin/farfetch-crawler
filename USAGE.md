# 快速使用指南

## 环境准备

1. **安装 Python 依赖**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **安装 Playwright 浏览器**
   ```bash
   python3 -m playwright install chromium
   ```

## 配置引导

### 方式一：交互式配置（推荐）

```bash
python3 setup_config.py
```

根据提示选择您的使用场景，工具会自动生成最佳配置。

### 方式二：手动配置

编辑 `playwright_crawler/config.py` 文件。详细配置说明请参考 [配置指南](CONFIG_GUIDE.md)。

**快速配置建议：**

**首次测试（显示浏览器窗口）：**
```python
HEADLESS = False
PAGE_LOAD_WAIT = (2000, 3000)
SCROLL_COUNT = (3, 5)
BETWEEN_PAGES = (2000, 3000)
```

**日常使用（推荐配置）：**
```python
HEADLESS = False
PAGE_LOAD_WAIT = (3000, 5000)
SCROLL_COUNT = (5, 8)
BETWEEN_PAGES = (5000, 10000)
```

**批量采集（无头模式）：**
```python
HEADLESS = True
PAGE_LOAD_WAIT = (5000, 8000)
SCROLL_COUNT = (5, 8)
BETWEEN_PAGES = (10000, 15000)
```

## 使用方法

### 方式一：命令行运行

```bash
# 快速测试（10个示例分类）
python3 -m playwright_crawler.batch_crawler data/服装分类_示例.csv

# 完整爬取（88个分类）
python3 -m playwright_crawler.batch_crawler data/服装分类_完整版.csv

# 重新提取分类
python3 -m playwright_crawler.extract_categories
```

### 方式二：交互式菜单

```bash
python3 quick_start.py
```

然后根据提示选择选项：
- 选项 1：快速测试
- 选项 2：完整爬取
- 选项 3：重新提取分类
- 选项 4：自定义任务文件

### 方式三：自定义任务

1. 创建 CSV 文件，格式如下：

```csv
一级分类,二级分类,网页链接,从第几页开始,到第几页为止
连衣裙,新娘礼服,https://www.farfetch.com/cn/shopping/women/bridal-dresses-1/items.aspx,1,2
```

2. 运行：
```bash
python3 -m playwright_crawler.batch_crawler 你的文件.csv
```

## 输出位置

所有数据保存在 `output/` 目录下：
- `output/batch_crawler.log` - 运行日志
- `output/一级分类/二级分类_第X页.csv` - 爬取的数据

## 查看日志

```bash
tail -f output/batch_crawler.log
```

## 配置调整

编辑 `playwright_crawler/config.py` 可以调整：
- 输出目录
- 反爬延时时间
- 是否无头模式运行

## 常见问题

### 1. 模块未找到
确保在项目根目录运行，使用 `-m` 方式：
```bash
cd /Users/zeus/Documents/farfetch-crawler
python3 -m playwright_crawler.batch_crawler data/服装分类_示例.csv
```

### 2. 浏览器启动失败
重新安装浏览器：
```bash
python3 -m playwright install --force chromium
```

### 3. 提取到 0 个商品
- 检查 URL 是否正确
- 手动打开 URL 确认商品显示
- 增加延时时间（修改 config.py）

详细文档请参考 [README.md](README.md)
