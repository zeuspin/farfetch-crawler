#!/usr/bin/env python3
"""
FARFETCH 批量爬虫（Playwright 版本）
根据CSV任务文件批量爬取商品数据

CSV格式:
一级分类,二级分类,网页链接,从第几页开始,到第几页为止
连衣裙,新娘礼服,https://www.farfetch.com/cn/shopping/women/bridal-dresses-1/items.aspx,1,2

反爬机制:
- 随机页面加载时间（3-5秒）
- 多次滚动触发懒加载（5-8次）
- 页面间随机延时（5-10秒）
- 任务间随机延时（5-10秒）
"""

import asyncio
import csv
import sys
from pathlib import Path

from playwright.async_api import async_playwright

from .config import (
    OUTPUT_BASE, HEADLESS, SLOW_MO, TIMEOUT,
    PAGE_LOAD_WAIT, SCROLL_COUNT, SCROLL_INTERVAL,
    BETWEEN_PAGES, BETWEEN_TASKS, BETWEEN_TASKS_SHORT,
    TEST_MODE, TEST_TIMEOUT
)
from .utils import (
    log, parse_farfetch_product, sanitize_filename,
    get_random_delay, save_products, load_tasks
)


# ==================== JavaScript 脚本 ====================
EXTRACT_PRODUCTS_SCRIPT = """() => {
  const products = [];
  const items = document.querySelectorAll('[data-component="ProductCard"]');

  items.forEach((item, index) => {
    try {
      const link = item.querySelector('a');
      const img = item.querySelector('img');

      if (!link) return;

      const text = link.textContent || '';
      const href = link.getAttribute('href') || '';
      const imgSrc = img?.getAttribute('src') || img?.getAttribute('data-src') || '';

      products.push({
        rawText: text,
        href: href,
        imgSrc: imgSrc
      });
    } catch (e) {
      // skip
    }
  });

  return products;
}"""


async def navigate_and_extract_page(page, url, page_num=1):
    """
    导航到页面并提取商品数据（含懒加载处理）
    
    Args:
        page: Playwright Page 对象
        url: 页面 URL
        page_num: 页码
        
    Returns:
        list: 商品列表
    """
    # 构建完整URL（带页码）
    if page_num > 1:
        separator = "&" if "?" in url else "?"
        target_url = f"{url}{separator}page={page_num}"
    else:
        target_url = url

    log(f"📍 导航到: {target_url}")
    
    import time
    start_time = time.time()
    
    # 根据测试模式选择超时时间
    actual_timeout = TEST_TIMEOUT if TEST_MODE else TIMEOUT
    if TEST_MODE:
        log(f"🧪 测试模式：使用超时时间 {actual_timeout}ms")

    try:
        # 导航到页面（使用 load 策略，比 networkidle 更宽松）
        goto_start = time.time()
        await page.goto(target_url, timeout=actual_timeout, wait_until="load")
        goto_time = int((time.time() - goto_start) * 1000)
        log(f"⏱️ 页面加载耗时: {goto_time}ms")

        # 反爬机制：随机等待页面加载
        wait_time = get_random_delay(PAGE_LOAD_WAIT)
        log(f"⏱️ 等待页面加载 {wait_time // 1000} 秒...")
        await page.wait_for_timeout(wait_time)

        # 反爬机制：多次滚动触发懒加载
        scroll_times = get_random_delay(SCROLL_COUNT)
        log(f"🔄 执行 {scroll_times} 次滚动触发懒加载...")

        scroll_script = "() => { window.scrollTo(0, document.body.scrollHeight); return 'scrolled'; }"
        scroll_start = time.time()
        for i in range(scroll_times):
            await page.evaluate(scroll_script)
            if i < scroll_times - 1:
                await page.wait_for_timeout(SCROLL_INTERVAL)
        scroll_time = int((time.time() - scroll_start) * 1000)
        log(f"⏱️ 滚动耗时: {scroll_time}ms")

        log("✅ 懒加载触发完成")

        # 提取商品数据
        extract_start = time.time()
        raw_data = await page.evaluate(EXTRACT_PRODUCTS_SCRIPT)
        extract_time = int((time.time() - extract_start) * 1000)
        log(f"✅ 提取到 {len(raw_data)} 个原始数据 (耗时: {extract_time}ms)")

        # 解析商品信息
        products = []
        for item in raw_data:
            parsed = parse_farfetch_product(item['rawText'], item['href'], item['imgSrc'])
            if parsed:
                products.append(parsed)

        # 统计总耗时
        total_time = int((time.time() - start_time) * 1000)
        log(f"✅ 成功解析 {len(products)} 个商品")
        log(f"⏱️ 本页总耗时: {total_time}ms ({total_time/1000:.1f}秒)")
        log(f"⏱️ 时间分布: 页面加载 {goto_time}ms + 滚动 {scroll_time}ms + 提取 {extract_time}ms")
        return products

    except Exception as e:
        log(f"❌ 页面处理异常: {e}")
        return []


async def process_task(page, level1, level2, url, start_page, end_page):
    """
    处理单个任务
    
    Args:
        page: Playwright Page 对象
        level1: 一级分类
        level2: 二级分类
        url: 页面 URL
        start_page: 起始页码
        end_page: 结束页码
        
    Returns:
        tuple: (总商品数, 成功页数, 失败页数, 是否有实际提取)
    """
    log(f"\n{'='*60}")
    log(f"开始处理任务: {level1} / {level2}")
    log(f"链接: {url}")
    log(f"页码范围: {start_page} - {end_page} (共{end_page - start_page + 1}页)")
    log(f"{'='*60}\n")

    # 创建一级分类文件夹
    safe_level1 = sanitize_filename(level1)
    level1_dir = OUTPUT_BASE / safe_level1
    level1_dir.mkdir(exist_ok=True)

    log(f"📁 创建文件夹: {level1_dir}")

    success_count = 0
    failed_count = 0
    total_products = 0
    consecutive_failures = 0
    skip_category = False

    # 逐页爬取
    for page_num in range(start_page, end_page + 1):
        if skip_category:
            log(f"⏭️ 跳过当前分类的剩余页面")
            break

        log(f"\n{'─'*40}")
        log(f"📄 处理第 {page_num}/{end_page} 页")
        log(f"{'─'*40}")

        # 检查文件是否已存在（断点续传）
        safe_level2 = sanitize_filename(level2)
        csv_filename = f"{safe_level2}_第{page_num}页.csv"
        csv_path = level1_dir / csv_filename

        if csv_path.exists():
            log(f"⏭️ 文件已存在，跳过: {csv_filename}")
            success_count += 1
            continue

        products = await navigate_and_extract_page(page, url, page_num)

        if products:
            # 保存 CSV 文件
            save_products(products, csv_path)

            success_count += 1
            total_products += len(products)
            consecutive_failures = 0
            log(f"✅ 第 {page_num} 页完成 - 保存到: {csv_filename}")
            log(f"   商品数: {len(products)}")
        else:
            log(f"❌ 第 {page_num} 页未提取到任何商品")
            consecutive_failures += 1
            log(f"⚠️ 连续失败次数: {consecutive_failures}")

            # 连续失败超过3次才跳过分类
            if consecutive_failures >= 3:
                log(f"⚠️ 连续失败{consecutive_failures}次，跳到下一个二级分类")
                skip_category = True
                break

        # 反爬机制：页面间延时
        if page_num < end_page:
            delay = get_random_delay(BETWEEN_PAGES)
            log(f"⏱️ 等待 {delay // 1000} 秒后继续下一页...")
            await asyncio.sleep(delay / 1000)

    log(f"\n✅ 任务完成！")
    log(f"   - 成功页数: {success_count}/{end_page - start_page + 1}")
    log(f"   - 失败页数: {failed_count}")
    log(f"   - 总商品数: {total_products}")
    log(f"   - 保存位置: {level1_dir}")

    has_actual_extraction = total_products > 0
    return total_products, success_count, failed_count, has_actual_extraction


async def run_batch(task_csv_path):
    """
    运行批量任务
    
    Args:
        task_csv_path: 任务 CSV 文件路径
    """
    log("🚀 FARFETCH 批量爬虫启动（Playwright 版本）")
    log(f"📋 任务文件: {task_csv_path}")
    log(f"📁 输出目录: {OUTPUT_BASE}\n")

    total_products = 0
    total_success = 0
    total_failed = 0
    task_count = 0

    try:
        # 加载任务
        tasks = load_tasks(task_csv_path)
        log(f"📊 共 {len(tasks)} 个任务\n")

        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(
                headless=HEADLESS,
                slow_mo=SLOW_MO
            )
            
            # 创建上下文和页面
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            page = await context.new_page()

            try:
                for task in tasks:
                    task_count += 1
                    level1 = task.get("一级分类", "").strip()
                    level2 = task.get("二级分类", "").strip()
                    url = task.get("网页链接", "").strip()

                    if not level1 or not level2 or not url:
                        log(f"⚠️ 跳过无效任务 {task_count}: 缺少必要字段")
                        continue

                    start_page = int(task.get("从第几页开始", "1"))
                    end_page = int(task.get("到第几页为止", task.get("总页数", "1")))

                    products, success, failed, has_extraction = await process_task(
                        page, level1, level2, url, start_page, end_page
                    )
                    total_products += products
                    total_success += success
                    total_failed += failed

                    log(f"\n📊 当前进度: {task_count}/{len(tasks)} 个任务")

                    # 反爬机制：只有实际进行了提取操作才需要任务间延时
                    if task_count < len(tasks) and has_extraction:
                        delay = get_random_delay(BETWEEN_TASKS)
                        log(f"\n⏱️ 任务间等待 {delay // 1000} 秒...")
                        await asyncio.sleep(delay / 1000)
                    elif task_count < len(tasks):
                        # 只是跳过文件，快速继续
                        await asyncio.sleep(BETWEEN_TASKS_SHORT / 1000)

            finally:
                await context.close()
                await browser.close()

    except FileNotFoundError as e:
        log(f"❌ 任务文件不存在: {task_csv_path}")
        log(f"   错误详情: {e}")
        return
    except Exception as e:
        import traceback
        log(f"❌ 批量任务异常: {e}")
        log(f"   错误详情: {traceback.format_exc()}")
        return

    # 总结
    log(f"\n{'='*60}")
    log(f"🎉 所有任务完成！")
    log(f"{'='*60}")
    log(f"📊 总任务数: {task_count}")
    log(f"📊 总成功页数: {total_success}")
    log(f"📊 总失败页数: {total_failed}")
    log(f"📦 总商品数: {total_products}")
    log(f"📁 数据位置: {OUTPUT_BASE}")


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python3 -m playwright_crawler.batch_crawler <任务CSV文件>")
        print("\nCSV格式:")
        print("一级分类,二级分类,网页链接,从第几页开始,到第几页为止")
        print("连衣裙,新娘礼服,https://www.farfetch.com/cn/...,1,2")
        sys.exit(1)

    task_csv = sys.argv[1]

    if not Path(task_csv).exists():
        print(f"❌ 文件不存在: {task_csv}")
        sys.exit(1)

    asyncio.run(run_batch(task_csv))


if __name__ == "__main__":
    main()
