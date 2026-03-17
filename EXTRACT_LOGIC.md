# make extract 命令执行逻辑

## 📋 概述

**命令：** `make extract`  
**执行文件：** `playwright_crawler/extract_categories.py`  
**主要功能：** 自动提取 FARFETCH 所有服装分类并生成 CSV 任务文件

---

## 🔄 详细执行流程

### 阶段 1: 初始化

```
开始
  ↓
确保 output/ 目录存在
  ↓
定义一级类目列表（11个）
  ├─ 连衣裙
  ├─ 裤子
  ├─ 上衣
  ├─ 半身裙
  ├─ 西装
  ├─ 短裤
  ├─ 夹克
  ├─ 外套
  ├─ 针织衫
  ├─ 连体衣/裤
  └─ 沙滩装
```

---

### 阶段 2: 启动浏览器

```
启动 Chromium 浏览器（Playwright）
  ↓
创建浏览器上下文
  ├─ 设置 User-Agent
  └─ 设置视口（1920x1080）
  ↓
创建页面
```

---

### 阶段 3: 遍历一级类目

```
对每个一级类目（共 11 个）：
  ↓
┌─────────────────────────────┐
│ 第 N 个一级类目（如"连衣裙"） │
└─────────────────────────────┘
  ↓
┌─────────────────────────────┐
│ 3.1 导航到一级类目页面      │
│   - URL: farfetch.com/...    │
│   - 等待加载（6-7秒）       │
└─────────────────────────────┘
  ↓
┌─────────────────────────────┐
│ 3.2 提取二级类目           │
│   - 执行 JavaScript 脚本    │
│   - 过滤、去重             │
│   - 返回二级类目列表         │
│                             │
│   结果示例：                 │
│   - 新娘礼服                 │
│   - 沙滩连衣裙               │
│   - 日常连衣裙               │
│   ...                       │
└─────────────────────────────┘
  ↓
如果没有二级类目？
  ├─ YES → 使用一级类目本身
  └─ NO  → 继续下一步
         ↓
┌─────────────────────────────┐
│ 3.3 对每个二级类目：        │
│   ├─ 3.3.1 导航到页面     │
│   ├─ 3.3.2 提取总页数     │
│   │   - 查找分页元素     │
│   │   - 解析 "1 / 86"     │
│   │   - 提取: 86        │
│   ├─ 3.3.3 保存结果       │
│   └─ 3.3.4 失败处理      │
└─────────────────────────────┘
  ↓
继续下一个一级类目...
```

---

### 阶段 4: 保存为 CSV

```
创建 CSV 文件
  ├─ 文件名: output/服装分类_所有二级类目.csv
  ├─ 编码: utf-8-sig（Excel 兼容）
  └─ 格式:
      一级分类,二级分类,网页链接,从第几页开始,到第几页为止
  ↓
写入所有记录
  - 记录总数: ~88-100 条
```

---

### 阶段 5: 关闭浏览器

```
关闭页面
  ↓
关闭上下文
  ↓
关闭浏览器
```

---

### 阶段 6: 显示统计

```
输出文件路径
  ↓
总记录数
  ↓
按一级类目分组统计
  ├─ 连衣裙: X 个二级类目
  ├─ 裤子: X 个二级类目
  ├─ 上衣: X 个二级类目
  └─ ...
```

---

## 🔍 JavaScript 脚本详解

### EXTRACT_LEVEL2_SCRIPT

**功能：** 从页面提取所有二级类目

```javascript
() => {
  const links = document.querySelectorAll("a[href*='/shopping/women/']");
  const subcategories = [];
  const seenNames = new Set();

  const excludePatterns = [
    'clothing-1', 'shoes-1', 'bags-purses-1',
    'accessories-all-1', 'jewellery-1', 'pre-owned-1',
    'sale', 'new-season'
  ];

  for (const link of links) {
    const href = link.getAttribute("href");
    const text = link.textContent?.trim();

    // 过滤条件
    if (href && text && text.length > 0 && text.length < 50) {
      if (!href.includes("/items.aspx")) continue;

      const parts = href.split('/');
      const secondLast = parts[parts.length - 2];

      // 检查是否是二级类目格式
      const isLevel2Format = secondLast && 
        secondLast.endsWith('-1') && 
        secondLast.includes('-');

      // 排除一级类目
      const isLevel1 = /^(dresses|trousers|tops|...)-1$/.test(secondLast);

      // 排除主导航
      const isMainNav = excludePatterns.some(pattern => secondLast === pattern);

      if (isLevel2Format && !isLevel1 && !isMainNav) {
        const cleanText = text.replace(/(.+)\\1/, '$1');

        // 去重
        if (!seenNames.has(cleanText)) {
          seenNames.add(cleanText);
          const fullUrl = href.startsWith("http") ? href : "https://www.farfetch.com" + href;
          subcategories.push({ name: cleanText, link: fullUrl });
        }
      }
    }
  }

  return subcategories;
}
```

---

### GET_PAGES_SCRIPT

**功能：** 从分页元素提取总页数

```javascript
() => {
  const result = { total_pages: 1 };
  
  // 方法1: 查找特定的分页元素
  const pageSpan = document.querySelector('.ltr-gq26dl, [class*="gq26dl"]');

  if (pageSpan) {
    const text = pageSpan.textContent?.trim();
    // 解析 "1 / 86" 格式
    const match = text.match(/(\\d+)\\s*\\/\\s*(\\d+)/);
    if (match) {
      result.total_pages = parseInt(match[2]);
      return result;
    }
  }

  // 方法2: 查找所有 span 元素
  const allSpans = document.querySelectorAll('span');
  for (const span of allSpans) {
    const text = span.textContent?.trim();
    if (text && text.includes(' / ')) {
      const match = text.match(/(\\d+)\\s*\\/\\s*(\\d+)/);
      if (match) {
        result.total_pages = parseInt(match[2]);
        return result;
      }
    }
  }

  return result;
}
```

---

## ⏱️ 时间估算

### 单个一级类目

| 操作 | 时间 | 说明 |
|------|------|------|
| 导航到一级类目 | ~7秒 | 包含加载等待 |
| 提取二级类目 | ~56秒 | 假设 8 个二级类目，每个 ~7秒 |
| 访问二级类目 | ~56秒 | 假设 8 个二级类目，每个 ~7秒 |
| **小计** | **~2分钟** | |

### 全部 11 个一级类目

| 操作 | 时间 |
|------|------|
| 单个一级类目平均 | 2分钟 |
| 全部 11 个 | **~22分钟** |
| 加上初始化和清理 | **~25分钟** |

---

## 📊 输出示例

### CSV 文件

```csv
一级分类,二级分类,网页链接,从第几页开始,到第几页为止
连衣裙,新娘礼服,https://www.farfetch.com/cn/shopping/women/bridal-dresses-1/items.aspx,1,2
连衣裙,沙滩连衣裙,https://www.farfetch.com/cn/shopping/women/beach-dresses-1/items.aspx,1,2
连衣裙,日常连衣裙,https://www.farfetch.com/cn/shopping/women/day-dresses-1/items.aspx,1,15
裤子,打底裤,https://www.farfetch.com/cn/shopping/women/leggings-1/items.aspx,1,3
上装,T恤,https://www.farfetch.com/cn/shopping/women/t-shirts-jersey-1/items.aspx,1,3
...
```

### 统计输出

```
============================================================
✅ 完成！
============================================================
输出文件: /Users/zeus/Documents/farfetch-crawler/output/服装分类_所有二级类目.csv
总记录数: 88

按一级类目统计:
  连衣裙: 12 个二级类目
  裤子: 8 个二级类目
  上衣: 10 个二级类目
  半身裙: 6 个二级类目
  ...
```

---

## 🎯 使用场景

### 场景 1: 定期更新分类

FARFETCH 分类可能定期更新：
- 新增商品分类
- 删除或合并分类
- 调整分类结构

**操作：** 定期运行 `make extract` 更新分类数据

---

### 场景 2: 扩展到其他类目

目前只支持服装类目，可以扩展支持：
- 鞋子类目
- 包包类目
- 配饰类目

**操作：** 修改 `LEVEL1_CATEGORIES` 列表

---

### 场景 3: 自定义分类

手动编辑提取结果：
- 添加感兴趣的分类
- 删除不需要的分类
- 调整页码范围

**操作：** 编辑生成的 CSV 文件

---

## ⚠️ 注意事项

### 1. 网络要求

- 需要能访问 farfetch.com
- 建议网络稳定
- 海外访问可能较慢

---

### 2. 失败处理

- 某个二级类目提取失败不会中断流程
- 失败的分类会标记为"需手动填写"
- 可以后续手动编辑 CSV 文件

---

### 3. 页数提取

- 从分页元素提取
- 如果找不到分页元素，默认为 1
- 某些分类可能只有 1 页

---

### 4. 输出文件

- 保存到 `output/` 目录
- 文件名：`服装分类_所有二级类目.csv`
- 可以直接用于 `make full` 或批量爬虫

---

## 🔧 相关配置

影响提取性能的配置（`playwright_crawler/config.py`）：

```python
# 页面加载等待时间（毫秒）
PAGE_LOAD_WAIT = (6000, 7000)  # 6-7秒

# 是否无头模式
HEADLESS = False  # False: 显示浏览器，True: 后台运行

# 页面超时时间（毫秒）
TIMEOUT = 90000  # 90秒，基于测试结果优化
```

修改这些配置会影响：
- 提取速度
- 超时频率
- 资源占用

---

## 📝 总结

`make extract` 命令执行逻辑：

1. **初始化** - 定义 11 个一级类目
2. **启动浏览器** - 使用 Playwright
3. **遍历一级类目** - 对每个一级类目提取二级类目
4. **提取二级类目** - 使用 JavaScript 查找和过滤
5. **获取总页数** - 从分页元素提取
6. **保存为 CSV** - 生成任务文件
7. **关闭浏览器** - 清理资源
8. **显示统计** - 输出分类数量

**预计时间：** ~25 分钟  
**输出文件：** `output/服装分类_所有二级类目.csv`  
**记录数：** ~88-100 条

---

**版本:** 2.0  
**最后更新:** 2026-03-17
