# Makefile 使用指南

本项目使用 Makefile 管理常用命令，简化日常操作。

---

## 📋 查看所有命令

```bash
make help
```

---

## 🚀 快速开始

### 1. 初始化环境（首次使用）

```bash
make setup
```

这会自动执行：
- 安装 Python 依赖（`pip3 install -r requirements.txt`）
- 安装 Playwright 浏览器（`python3 -m playwright install chromium`）

### 2. 配置爬虫

```bash
make setup-config
```

根据向导完成配置。

### 3. 验证环境

```bash
make check
```

检查 Python、Playwright、数据文件等是否就绪。

### 4. 运行测试

```bash
make quick
```

运行快速测试（10个示例分类）。

---

## 📝 常用命令

### 环境管理

| 命令 | 说明 |
|------|------|
| `make setup` | 初始化环境（依赖 + 浏览器） |
| `make install` | 安装 Python 依赖 |
| `make install-browser` | 安装 Playwright 浏览器 |
| `make update-browser` | 更新 Playwright 浏览器 |
| `make check` | 检查环境和依赖 |

### 配置管理

| 命令 | 说明 |
|------|------|
| `make setup-config` | 运行配置引导工具 |
| `make show-config` | 显示当前配置 |
| `make restore-config` | 恢复配置文件备份 |

### 爬虫运行

| 命令 | 说明 |
|------|------|
| `make test` | 运行验证测试 |
| `make quick` | 快速测试（10个示例分类） |
| `make full` | 完整爬取（88个分类） |
| `make extract` | 重新提取分类 |
| `make interactive` | 交互式菜单 |

### 日志和统计

| 命令 | 说明 |
|------|------|
| `make log` | 查看运行日志（实时，按 Ctrl+C 退出） |
| `make log-last` | 查看最后 50 行日志 |
| `make stats` | 查看输出统计 |

### 清理

| 命令 | 说明 |
|------|------|
| `make clean-output` | 清理输出文件（保留日志） |
| `make clean-all` | 清理所有输出（包括日志） |

### 其他

| 命令 | 说明 |
|------|------|
| `make docs` | 查看可用文档 |
| `make help` | 显示帮助信息 |

---

## 📊 使用示例

### 场景 1: 首次使用

```bash
# 1. 初始化环境
make setup

# 2. 配置爬虫
make setup-config

# 3. 验证环境
make check

# 4. 快速测试
make quick
```

### 场景 2: 日常使用

```bash
# 查看当前配置
make show-config

# 快速测试
make quick

# 查看日志
make log-last
```

### 场景 3: 完整爬取

```bash
# 先快速测试确认无误
make quick

# 查看日志确认正常
make log-last

# 开始完整爬取
make full

# 在另一个终端监控日志
make log
```

### 场景 4: 监控运行

```bash
# 终端 1: 启动爬虫
make full

# 终端 2: 查看日志
make log

# 终端 3: 查看统计
make stats
```

---

## 🎯 命令详解

### make setup

初始化环境，包括：
- 安装 Python 依赖
- 安装 Chromium 浏览器

```bash
make setup
```

---

### make setup-config

运行交互式配置引导工具，引导您完成以下步骤：
1. 选择使用场景
2. 配置浏览器显示模式
3. 选择网络环境
4. 设置懒加载策略
5. 自定义参数（可选）

```bash
make setup-config
```

---

### make quick

快速测试，爬取 10 个示例分类。

```bash
make quick
```

**预期时间：** 约 1-2 分钟

---

### make full

完整爬取，爬取 88 个分类。

```bash
make full
```

**预期时间：** 约 1-2 小时

**注意：** 运行前会要求确认，避免误操作。

---

### make log

实时查看运行日志，按 Ctrl+C 退出。

```bash
make log
```

**使用场景：**
- 爬虫运行时监控进度
- 排查问题查看详细日志

---

### make stats

查看输出统计信息，包括：
- 输出目录大小
- CSV 文件数量
- 分类目录数量
- 各分类文件数

```bash
make stats
```

---

### make clean-output

清理所有爬取的数据文件，保留日志文件。

```bash
make clean-output
```

**注意：** 会要求确认，避免误删除数据。

---

### make clean-all

清理所有输出文件和日志。

```bash
make clean-all
```

**注意：** 会要求确认，避免误删除数据。

---

## 💡 小技巧

### 1. 查看当前配置

```bash
make show-config
```

### 2. 快速检查环境

```bash
make check
```

### 3. 修改配置后查看

```bash
make setup-config  # 配置
make show-config   # 确认
make quick         # 测试
```

### 4. 批量操作

```bash
# 查看最后日志
make log-last

# 查看统计
make stats

# 清理输出
make clean-output
```

---

## 🛠️ 故障排查

### 问题：make 命令不存在

**解决方案：**
```bash
# macOS
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential
```

### 问题：make 没有找到 Python 依赖

**解决方案：**
```bash
# 手动安装
pip3 install -r requirements.txt
```

### 问题：Chromium 浏览器未安装

**解决方案：**
```bash
make install-browser
```

### 问题：配置文件损坏

**解决方案：**
```bash
make restore-config
```

---

## 📚 更多信息

- **完整文档：** [README.md](README.md)
- **快速指南：** [USAGE.md](USAGE.md)
- **配置指南：** [CONFIG_GUIDE.md](CONFIG_GUIDE.md)

---

**版本:** 1.0  
**最后更新:** 2026-03-17
