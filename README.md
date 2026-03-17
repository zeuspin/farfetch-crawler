# FARFETCH 数据爬虫（Playwright 版本）

基于 Playwright 的 FARFETCH 商品数据批量爬取工具，支持服装、女鞋等多个类目，完全脱离 OpenClaw 运行环境。

## 📦 特性

- ✅ **零依赖 OpenClaw**：使用 Playwright 替代，无需安装 Node.js 和 OpenClaw
- ✅ **功能完整**：保留所有原有功能（分类提取、批量爬取、断点续传）
- ✅ **反爬机制**：随机延时、懒加载触发、智能等待
- ✅ **易于部署**：纯 Python 环境，一键安装依赖

## 🚀 快速开始

### 1. 安装依赖（推荐使用 Makefile）

```bash
# 方式一：使用 Makefile（推荐）
make setup

# 方式二：手动安装
pip install -r requirements.txt
python3 -m playwright install chromium
```

### 2. 配置参数（可选）

首次使用推荐使用交互式配置引导：

```bash
# 方式一：使用 Makefile
make setup-config

# 方式二：直接运行脚本
python3 setup_config.py
```

配置引导会根据您的使用场景智能推荐参数，包括：
- 使用场景（快速测试/小规模/大规模/服务器）
- 浏览器显示模式（有头/无头）
- 网络环境
- 懒加载策略

或者手动编辑 `playwright_crawler/config.py` 文件。详细说明请参考 [配置指南](CONFIG_GUIDE.md)。

### 3. 验证环境

```bash
# 使用 Makefile
make check

# 或运行验证脚本
python3 test.py
```

### 4. 运行爬虫

#### 方式一：使用预提取的分类数据（推荐）

**服装类目：**

```bash
# 使用 Makefile（推荐）
make quick      # 快速测试（10个示例分类）
make full       # 完整运行（88个分类）

# 或使用命令行
python3 -m playwright_crawler.batch_crawler data/服装分类_示例.csv
python3 -m playwright_crawler.batch_crawler data/服装分类_完整版.csv
```

**女鞋类目：**

```bash
# 使用 Makefile（推荐）
make quick-shoes    # 快速测试女鞋类目（3个示例分类）
make full-shoes     # 完整运行女鞋类目（26个分类）

# 或使用命令行
python3 -m playwright_crawler.batch_crawler data/女鞋类目.csv
```

⚠️ **注意：** 爬虫是通用的，可以爬取 FARFETCH 的任何类目，只需提供对应格式的 CSV 文件。

#### 方式二：重新提取分类

```bash
# 使用 Makefile
make extract

# 或使用命令行
python3 -m playwright_crawler.extract_categories

# 输出文件：output/服装分类_所有二级类目.csv
# 然后运行批量爬虫
python3 -m playwright_crawler.batch_crawler output/服装分类_所有二级类目.csv
```

#### 方式三：自定义任务

1. 创建你自己的 CSV 文件，格式如下：

```csv
一级分类,二级分类,网页链接,从第几页开始,到第几页为止
连衣裙,新娘礼服,https://www.farfetch.com/cn/shopping/women/bridal-dresses-1/items.aspx,1,2
上装,T恤,https://www.farfetch.com/cn/shopping/women/t-shirts-jersey-1/items.aspx,1,5
```

2. 运行爬虫：
```bash
python3 -m playwright_crawler.batch_crawler 你的任务文件.csv
```

## 📁 项目结构

```
farfetch-crawler/
├── playwright_crawler/          # 核心代码
│   ├── __init__.py
│   ├── config.py               # 配置文件
│   ├── utils.py                # 工具函数
│   ├── extract_categories.py   # 分类提取
│   └── batch_crawler.py        # 批量爬虫
├── data/                       # 数据目录
│   ├── 服装分类_示例.csv       # 10条示例
│   ├── 服装分类_完整版.csv     # 88条完整数据
│   └── 女鞋类目.csv            # 26个女鞋分类
├── output/                     # 输出目录
│   ├── batch_crawler.log       # 运行日志
│   ├── 连衣裙/
│   ├── 上装/
│   └── ...
├── logs/                       # 日志目录
├── Makefile                    # 命令管理
├── MAKEFILE_GUIDE.md           # Makefile 使用指南
├── SHOES_GUIDE.md             # 女鞋类目使用指南
└── requirements.txt            # 依赖清单
```

## 🔧 使用 Makefile（推荐）

本项目提供了 Makefile 来简化常用命令管理。

### 查看所有命令

```bash
make help
```

### 常用命令

| 命令 | 说明 |
|------|------|
| `make setup` | 初始化环境 |
| `make setup-config` | 运行配置引导 |
| `make check` | 检查环境 |
| `make test` | 运行验证测试 |
| `make quick` | 快速测试（10个示例） |
| `make full` | 完整爬取（88个分类） |
| `make extract` | 重新提取分类 |
| `make log` | 查看运行日志（实时） |
| `make stats` | 查看输出统计 |
| `make clean-output` | 清理输出文件 |
| `make show-config` | 显示当前配置 |

### 典型工作流

```bash
# 1. 初始化环境
make setup

# 2. 配置爬虫
make setup-config

# 3. 验证环境
make check

# 4. 快速测试
make quick

# 5. 查看日志
make log-last
```

详细使用指南请参考 [Makefile 使用指南](MAKEFILE_GUIDE.md)。

## 📊 输出结构

```
output/
├── batch_crawler.log              # 运行日志
├── 连衣裙/
│   ├── 新娘礼服_第1页.csv         # 每页一个文件
│   ├── 新娘礼服_第2页.csv
│   └── 日常连衣裙_第1页.csv
├── 上装/
│   ├── T恤_第1页.csv
│   └── ...
└── 裤子/
    └── ...
```

**CSV数据格式：**
```csv
品牌,商品标题,价格,商品链接,商品主图地址
Brand A,商品名称 A,¥1,200,https://...,https://...
Brand B,商品名称 B,¥890,https://...,https://...
```

## ⚙️ 配置说明

### 修改配置

编辑 `playwright_crawler/config.py`：

```python
# 输出目录
OUTPUT_BASE = Path(__file__).parent.parent / "output"

# 反爬延时配置（毫秒）
PAGE_LOAD_WAIT = (3000, 5000)      # 页面加载等待 3-5秒
SCROLL_COUNT = (5, 8)              # 滚动 5-8次
BETWEEN_PAGES = (5000, 10000)      # 页面间 5-10秒
BETWEEN_TASKS = (5000, 10000)      # 任务间 5-10秒

# 浏览器配置
HEADLESS = False                   # 是否无头模式
SLOW_MO = 0                        # 慢动作模式（毫秒）
```

### 无头模式

如需在服务器上运行，设置为 `True`：

```python
HEADLESS = True
```

## 🛠️ 反爬机制

脚本内置以下反爬策略：

- **页面加载**：3-5秒随机等待
- **懒加载触发**：5-8次滚动
- **页面间延时**：5-10秒随机
- **任务间延时**：5-10秒随机
- **User-Agent**：模拟真实浏览器

## 📝 运行监控

### 实时查看日志
```bash
tail -f output/batch_crawler.log
```

### 时间估算

- 每页约 10-15 秒（含延时）
- 100 页约需 25-30 分钟
- 建议分批处理大量任务

## ⚠️ 注意事项

1. **网络稳定性**
   - 确保网络连接稳定
   - 长时间运行建议使用代理

2. **频率控制**
   - 不建议同时运行多个爬虫实例
   - 如需加速，适当减少延时时间

3. **数据备份**
   - 定期备份已爬取的数据
   - 日志文件可用于排查问题

4. **浏览器版本**
   - Playwright 会自动管理 Chromium 版本
   - 如遇问题，运行 `playwright install --force chromium`

## 🆘 故障排除

### 问题：模块未找到

**解决方法：**
```bash
# 确保在项目根目录
cd /Users/zeus/Documents/farfetch-crawler

# 使用 -m 方式运行
python3 -m playwright_crawler.batch_crawler data/服装分类_示例.csv
```

### 问题：浏览器启动失败

**解决方法：**
```bash
# 重新安装浏览器
playwright install --force chromium
```

### 问题：提取到 0 个商品

**可能原因：**
1. 页面结构变化
2. 页面加载未完成
3. URL 错误

**解决方法：**
1. 检查 URL 是否正确
2. 手动打开 URL 确认商品显示
3. 增加延时（修改 config.py 中的等待时间）

### 问题：任务文件编码问题

**解决方法：**
- 使用 UTF-8 编码保存 CSV
- 或使用 UTF-8 with BOM (`utf-8-sig`)
- Excel 另存为"CSV UTF-8"格式

## 📄 文件说明

| 文件 | 说明 |
|------|------|
| `config.py` | 配置文件（路径、延时、浏览器设置） |
| `utils.py` | 工具函数（日志、商品解析、文件操作） |
| `extract_categories.py` | 分类提取工具 |
| `batch_crawler.py` | 批量爬虫主程序 |
| `服装分类_完整版.csv` | 预提取的分类数据（88个二级分类） |
| `服装分类_示例.csv` | 示例任务文件（10条数据） |

## 🔄 与原版对比

| 特性 | OpenClaw 版 | Playwright 版 |
|------|-----------|---------------|
| 安装依赖 | npm install -g openclaw + 插件 | pip install -r requirements.txt |
| 浏览器控制 | OpenClaw Browser Relay | Playwright 原生 |
| 启动方式 | 启动 Relay + 安装插件 | 直接运行 Python |
| 无头模式 | ❌ 不支持 | ✅ 支持 |
| 部署复杂度 | 高（需要 Node.js + 插件） | 低（只需 Python） |
| 功能完整性 | ✅ 100% | ✅ 100% |

## 💡 使用技巧

1. **快速测试**
   - 先用 `服装分类_示例.csv` 测试
   - 确认无误后再处理完整数据

2. **分批处理**
   - 将大任务拆分成多个小任务
   - 避免单次运行时间过长

3. **监控进度**
   - 使用 `tail -f` 实时查看日志
   - 检查 output 目录确认数据生成

4. **数据校验**
    - 随机抽查 CSV 文件内容
    - 确认品牌、价格等字段完整

---

## 👟 支持的类目

### 服装类目

**数据文件：**
- `data/服装分类_示例.csv` - 10 条测试数据
- `data/服装分类_完整版.csv` - 88 条完整数据

**使用方式：**
```bash
make quick      # 快速测试
make full       # 完整爬取
```

**详细说明：** 见本文档"运行爬虫"部分

---

### 女鞋类目

**数据文件：**
- `data/女鞋类目.csv` - 26 个女鞋分类

**主要类目：**
- Boots（靴子）- 机车靴、及膝靴、过膝靴、及踝靴等
- 穆勒鞋 - 平底穆勒鞋、高跟穆勒鞋
- 草编鞋 - 平底草编鞋、高跟草编鞋
- 高跟鞋 - 平底鞋、高跟鞋
- 凉鞋 - 平底凉鞋、高跟凉鞋
- 运动鞋 - 低帮鞋、高帮鞋、套穿鞋
- 其他 - 德比鞋、乐福鞋、芭蕾平底鞋等

**使用方式：**
```bash
make quick-shoes   # 快速测试（3个示例）
make full-shoes    # 完整爬取（26个分类）
```

**详细说明：** [鞋子类目使用指南](SHOES_GUIDE.md)

---

### 自定义类目

爬虫支持 FARFETCH 的任何类目，只需提供对应格式的 CSV 文件：

```csv
一级分类,二级分类,网页链接,从第几页开始,到第几页为止
自定义分类,自定义子分类,https://www.farfetch.com/cn/...,1,10
```

运行方式：
```bash
python3 -m playwright_crawler.batch_crawler 你的CSV文件.csv
```

---

## 🆘 获取帮助

如遇问题，请检查：
1. 日志文件 `output/batch_crawler.log`
2. 确保已安装 Playwright：`playwright install chromium`
3. 检查 CSV 文件格式是否正确

---

**Version 2.0** - Powered by Playwright 🎭
