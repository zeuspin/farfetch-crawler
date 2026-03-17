#!/usr/bin/env python3
"""
FARFETCH 分类提取工具（Playwright 版本）
自动提取所有一级类目及其二级类目
"""

import asyncio
import csv
from pathlib import Path

from playwright.async_api import async_playwright

from .config import (
    BASE_DIR, DATA_DIR, OUTPUT_DIR,
    PAGE_LOAD_WAIT, HEADLESS, SLOW_MO, TIMEOUT
)
from .utils import log


# ==================== JavaScript 脚本 ====================
EXTRACT_LEVEL2_SCRIPT = """() => {
  const links = document.querySelectorAll("a[href*='/shopping/women/']");
  const subcategories = [];
  const seenNames = new Set();

  const excludePatterns = [
    'clothing-1', 'shoes-1', 'bags-purses-1', 'accessories-all-1',
    'jewellery-1', 'pre-owned-1', 'sale', 'new-season'
  ];

  for (const link of links) {
    const href = link.getAttribute("href");
    const text = link.textContent?.trim();

    if (href && text && text.length > 0 && text.length < 50) {
      if (!href.includes("/items.aspx")) continue;

      const parts = href.split('/');
      const secondLast = parts[parts.length - 2];

      const isLevel2Format = secondLast && secondLast.endsWith('-1') && secondLast.includes('-');
      const isLevel1 = /^(dresses|trousers|tops|skirts|shorts|jackets|coats|knitwear|suits|all-in-one|beachwear|leggings)-1$/.test(secondLast);
      const isMainNav = excludePatterns.some(pattern => secondLast === pattern);

      if (isLevel2Format && !isLevel1 && !isMainNav) {
        const cleanText = text.replace(/(.+)\\1/, '$1');

        if (!seenNames.has(cleanText)) {
          seenNames.add(cleanText);
          const fullUrl = href.startsWith("http") ? href : "https://www.farfetch.com" + href;
          subcategories.push({ name: cleanText, link: fullUrl });
        }
      }
    }
  }

  return subcategories;
}"""

GET_PAGES_SCRIPT = """() => {
  const result = { total_pages: 1 };
  const pageSpan = document.querySelector('.ltr-gq26dl, [class*="gq26dl"]');

  if (pageSpan) {
    const text = pageSpan.textContent?.trim();
    const match = text.match(/(\\d+)\\s*\\/\\s*(\\d+)/);
    if (match) {
      result.total_pages = parseInt(match[2]);
      return result;
    }
  }

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
}"""


async def navigate_to(page, url):
    """
    导航到 URL 并等待加载
    
    Args:
        page: Playwright Page 对象
        url: 目标 URL
    """
    await page.goto(url, timeout=TIMEOUT, wait_until="networkidle")
    # 随机等待页面加载
    from .utils import get_random_delay
    wait_time = get_random_delay(PAGE_LOAD_WAIT)
    await page.wait_for_timeout(wait_time)


async def run_script(page, script):
    """
    执行 JavaScript 脚本
    
    Args:
        page: Playwright Page 对象
        script: JavaScript 脚本字符串
        
    Returns:
        脚本执行结果
    """
    return await page.evaluate(script)


async def extract_categories():
    """
    主函数：提取所有分类
    """
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 一级类目列表
    LEVEL1_CATEGORIES = [
        {"name": "连衣裙", "url": "https://www.farfetch.com/sg/shopping/women/dresses-1/items.aspx"},
        {"name": "裤子", "url": "https://www.farfetch.com/sg/shopping/women/trousers-1/items.aspx"},
        {"name": "上衣", "url": "https://www.farfetch.com/sg/shopping/women/tops-1/items.aspx"},
        {"name": "半身裙", "url": "https://www.farfetch.com/sg/shopping/women/skirts-1/items.aspx"},
        {"name": "西装", "url": "https://www.farfetch.com/sg/shopping/women/suits-1/items.aspx"},
        {"name": "短裤", "url": "https://www.farfetch.com/sg/shopping/women/shorts-1/items.aspx"},
        {"name": "夹克", "url": "https://www.farfetch.com/sg/shopping/women/jackets-1/items.aspx"},
        {"name": "外套", "url": "https://www.farfetch.com/sg/shopping/women/coats-1/items.aspx"},
        {"name": "针织衫", "url": "https://www.farfetch.com/sg/shopping/women/knitwear-1/items.aspx"},
        {"name": "连体衣/裤", "url": "https://www.farfetch.com/sg/shopping/women/all-in-one-1/items.aspx"},
        {"name": "沙滩装", "url": "https://www.farfetch.com/sg/shopping/women/beachwear-1/items.aspx"},
    ]

    log("=" * 80)
    log("开始提取所有服装分类（Playwright 版本）")
    log("=" * 80)

    all_results = []

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
            for i, level1 in enumerate(LEVEL1_CATEGORIES, 1):
                log(f"\n[{i}/{len(LEVEL1_CATEGORIES)}] {level1['name']}")
                log("-" * 60)

                try:
                    # 导航到一级类目页面
                    log(f"  导航到 {level1['name']}...")
                    await navigate_to(page, level1['url'])

                    # 提取二级类目
                    log(f"  提取二级类目...")
                    level2_cats = await run_script(page, EXTRACT_LEVEL2_SCRIPT)

                    if not level2_cats:
                        log(f"  ℹ️ 没有找到二级类目，记录一级类目本身")
                        level2_cats = [{"name": level1['name'], "link": level1['url']}]
                    else:
                        log(f"  找到 {len(level2_cats)} 个二级类目")

                    # 对每个二级类目提取总页数
                    for j, level2 in enumerate(level2_cats, 1):
                        print(f"    [{j}/{len(level2_cats)}] {level2['name']:<30}", end="")

                        try:
                            # 导航到二级类目
                            await navigate_to(page, level2['link'])

                            # 获取总页数
                            pages_data = await run_script(page, GET_PAGES_SCRIPT)
                            total_pages = pages_data.get('total_pages', 1) if pages_data else 1

                            all_results.append({
                                "一级分类": level1['name'],
                                "二级分类": level2['name'],
                                "网页链接": level2['link'],
                                "从第几页开始": 1,
                                "到第几页为止": total_pages
                            })

                            print(f" -> {total_pages} 页")

                        except Exception as e:
                            print(f" -> ❌ 失败")
                            log(f"      错误: {e}")
                            all_results.append({
                                "一级分类": level1['name'],
                                "二级分类": level2['name'],
                                "网页链接": level2['link'],
                                "从第几页开始": 1,
                                "到第几页为止": "需手动填写"
                            })

                except Exception as e:
                    log(f"  ❌ 处理失败: {e}")

        finally:
            await context.close()
            await browser.close()

    # 保存为 CSV
    output_file = OUTPUT_DIR / "服装分类_所有二级类目.csv"
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["一级分类", "二级分类", "网页链接", "从第几页开始", "到第几页为止"])
        writer.writeheader()
        writer.writerows(all_results)

    log(f"\n{'='*80}")
    log(f"✅ 完成！")
    log(f"{'='*80}")
    log(f"输出文件: {output_file}")
    log(f"总记录数: {len(all_results)}")
    log()

    # 按一级类目分组统计
    from collections import defaultdict
    level1_stats = defaultdict(int)
    for row in all_results:
        level1_stats[row['一级分类']] += 1

    log("按一级类目统计:")
    for level1, count in level1_stats.items():
        log(f"  {level1}: {count} 个二级类目")


def main():
    """命令行入口"""
    asyncio.run(extract_categories())


if __name__ == "__main__":
    main()
