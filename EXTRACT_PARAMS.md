# 分类提取参数化说明

## 📋 概述

从硬编码 URL 改为参数化，支持：
- 指定基础 URL 域名（cn/sg/us/uk）
- 只提取指定的一级类目
- 自定义输出文件名

---

## 🚀 使用方法

### 方式一：使用 Makefile

```bash
# 提取所有分类（默认 cn 域名）
make extract

# 使用 sg 域名
make extract-sg

# 使用 cn 域名
make extract-cn

# 只提取连衣裙
make extract-dresses

# 只提取裤子
make extract-pants
```

---

### 方式二：使用命令行参数

#### 1. 指定域名

```bash
# 使用 cn 域名（默认）
python3 -m playwright_crawler.extract_categories --base-url cn

# 使用 sg 域名
python3 -m playwright_crawler.extract_categories --base-url sg

# 使用 us 域名
python3 -m playwright_crawler.extract_categories --base-url us

# 使用 uk 域名
python3 -m playwright_crawler.extract_categories --base-url uk
```

---

#### 2. 指定类目

```bash
# 只提取连衣裙
python3 -m playwright_crawler.extract_categories --categories 连衣裙

# 提取多个类目（逗号分隔）
python3 -m playwright_crawler.extract_categories --categories 连衣裙,裤子,上装

# 提取所有类目
python3 -m playwright_crawler.extract_categories
```

---

#### 3. 指定输出文件

```bash
# 指定输出文件名
python3 -m playwright_crawler.extract_categories --output 我的分类.csv

# 指定带域名的输出文件
python3 -m playwright_crawler.extract_categories --base-url sg --output sg分类.csv
```

---

#### 4. 组合使用

```bash
# sg 域名 + 只提取连衣裙和裤子 + 自定义文件名
python3 -m playwright_crawler.extract_categories --base-url sg --categories 连衣裙,裤子 --output sg连衣裙裤子.csv

# cn 域名 + 只提取上装 + 自定义文件名
python3 -m playwright_crawler.extract_categories --base-url cn --categories 上装 --output cn上装.csv
```

---

## 📊 可用类目

以下类目可以作为 `--categories` 参数：

| 类目 | 说明 |
|------|------|
| 连衣裙 | Dress |
| 裤子 | Trousers |
| 上衣 | Tops |
| 半身裙 | Skirts |
| 西装 | Suits |
| 短裤 | Shorts |
| 夹克 | Jackets |
| 外套 | Coats |
| 针织衫 | Knitwear |
| 连体衣/裤 | All-in-One |
| 沙滩装 | Beachwear |

---

## 📋 Makefile 命令

| 命令 | 说明 |
|------|------|
| `make extract` | 提取所有分类（cn 域名） |
| `make extract-sg` | 提取所有分类（sg 域名） |
| `make extract-cn` | 提取所有分类（cn 域名） |
| `make extract-dresses` | 只提取连衣裙 |
| `make extract-pants` | 只提取裤子 |

---

## 🔧 参数详解

### `--base-url`

指定 FARFETCH 的基础 URL 域名。

**支持值：**
- `cn`: 中国（默认）
- `sg`: 新加坡
- `us`: 美国
- `uk`: 英国

**示例：**
```bash
python3 -m playwright_crawler.extract_categories --base-url sg
```

---

### `--categories`

指定要提取的一级类目，逗号分隔。

**示例：**
```bash
# 单个类目
--categories 连衣裙

# 多个类目
--categories 连衣裙,裤子,上装
```

**注意：**
- 如果不指定，则提取所有类目
- 类目名称必须与可用类目列表一致

---

### `--output`

指定输出文件名。

**示例：**
```bash
--output 我的分类.csv
--output sg连衣裙.csv
```

**注意：**
- 如果不指定，默认为 `服装分类_所有二级类目.csv`
- 文件会保存到 `output/` 目录

---

## 📝 URL 生成规则

URL 格式：
```
https://www.farfetch.com/{base_url}/shopping/women/{category}-1/items.aspx
```

**示例：**

| base_url | category | URL |
|----------|----------|-----|
| cn | dresses | https://www.farfetch.com/cn/shopping/women/dresses-1/items.aspx |
| sg | trousers | https://www.farfetch.com/sg/shopping/women/trousers-1/items.aspx |
| us | tops | https://www.farfetch.com/us/shopping/women/tops-1/items.aspx |

---

## 💡 使用场景

### 场景 1: 不同地区的价格

```bash
# 提取 cn 域名的价格
python3 -m playwright_crawler.extract_categories --base-url cn --output cn_分类.csv

# 提取 sg 域名的价格
python3 -m playwright_crawler.extract_categories --base-url sg --output sg_分类.csv

# 对比两个地区的价格
# 分别使用两个 CSV 文件运行批量爬虫
```

---

### 场景 2: 只提取需要的类目

```bash
# 只提取连衣裙、裤子和上装
python3 -m playwright_crawler.extract_categories --categories 连衣裙,裤子,上装 --output 主要类目.csv

# 只提取夏季类目
python3 -m playwright_crawler.extract_categories --categories 连衣裙,半身裙,短裤,沙滩装 --output 夏季类目.csv
```

---

### 场景 3: 测试和验证

```bash
# 先测试一个小类目
python3 -m playwright_crawler.extract_categories --categories 连衣裙 --output 测试.csv

# 确认无误后，再提取所有类目
make extract
```

---

## ⚠️ 注意事项

1. **类目名称**
   - 必须与可用类目列表一致
   - 区分大小写
   - 不能有空格

2. **域名选择**
   - cn: 中国大陆
   - sg: 新加坡
   - us: 美国
   - uk: 英国

3. **文件名**
   - 文件会保存到 `output/` 目录
   - 相同文件名会被覆盖
   - 建议使用有意义的文件名

---

## 🎯 推荐工作流

### 工作流 1: 标准流程

```bash
# 1. 提取所有分类
make extract

# 2. 查看输出
ls output/

# 3. 运行批量爬虫
make quick
```

---

### 工作流 2: 测试验证

```bash
# 1. 先测试小类目
python3 -m playwright_crawler.extract_categories --categories 连衣裙 --output 测试.csv

# 2. 运行测试爬取
python3 -m playwright_crawler.batch_crawler output/测试.csv

# 3. 确认无误
# 4. 提取所有类目
make extract
```

---

### 工作流 3: 多地区对比

```bash
# 1. 提取 cn 域名分类
python3 -m playwright_crawler.extract_categories --base-url cn --output cn_分类.csv

# 2. 提取 sg 域名分类
python3 -m playwright_crawler.extract_categories --base-url sg --output sg_分类.csv

# 3. 分别爬取两个地区的价格
make clean-output
python3 -m playwright_crawler.batch_crawler output/cn_分类.csv
make clean-output
python3 -m playwright_crawler.batch_crawler output/sg_分类.csv
```

---

## 📚 相关文档

- [README.md](README.md) - 完整使用文档
- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - 配置指南
- [MAKEFILE_GUIDE.md](MAKEFILE_GUIDE.md) - Makefile 使用指南

---

**版本:** 2.0  
**最后更新:** 2026-03-17
