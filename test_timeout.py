#!/usr/bin/env python3
"""
超时时间测试工具
测试不同的超时时间设置，找出最优值
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from playwright_crawler import config


def test_timeout(timeout_ms):
    """测试指定的超时时间"""
    print(f"\n{'='*60}")
    print(f"🧪 测试超时时间: {timeout_ms}ms ({timeout_ms/1000:.1f}秒)")
    print(f"{'='*60}")
    
    # 修改配置
    config.TIMEOUT = timeout_ms
    config.TEST_MODE = True
    config.TEST_TIMEOUT = timeout_ms
    
    print(f"✅ 配置已更新")
    print(f"   超时时间: {timeout_ms}ms")
    print(f"   测试模式: True")
    
    print(f"\n📋 测试命令:")
    print(f"   python3 -m playwright_crawler.batch_crawler data/女鞋类目_测试3条.csv")
    
    print(f"\n💡 测试建议:")
    print(f"   1. 运行上述命令")
    print(f"   2. 观察日志中的'页面加载耗时'")
    print(f"   3. 如果出现超时，增加超时时间")
    print(f"   4. 如果没有超时且加载时间稳定，可以尝试降低超时时间")
    print(f"   5. 目标：找到既能避免超时，又不会浪费时间的超时值")


def main():
    """主函数"""
    print("╔" + "═"*58 + "╗")
    print("║" + " "*15 + "🔍 FARFETCH 超时时间测试工具" + " "*15 + "║")
    print("╚" + "═"*58 + "╝")
    
    print("\n📊 测试策略：")
    print("   从小到大测试不同的超时时间")
    print("   找出既能避免超时，又不会浪费时间的最优值")
    
    print("\n🎯 推荐测试顺序：")
    print("   1. 60000ms (60秒) - 快速，可能超时")
    print("   2. 90000ms (90秒) - 中等")
    print("   3. 120000ms (120秒) - 当前默认值")
    print("   4. 180000ms (180秒) - 保守")
    
    print("\n⚙️  配置说明：")
    print(f"   当前默认超时: {config.TIMEOUT}ms")
    print(f"   测试模式: {config.TEST_MODE}")
    
    print("\n🚀 选择测试选项：")
    print("   1. 测试 60000ms (60秒) - 快速测试")
    print("   2. 测试 90000ms (90秒) - 中等测试")
    print("   3. 测试 120000ms (120秒) - 当前默认")
    print("   4. 测试 180000ms (180秒) - 保守测试")
    print("   5. 测试 240000ms (240秒) - 极保守")
    print("   6. 自定义超时时间")
    print("   0. 退出")
    
    choice = input("\n请选择 [0-6]: ").strip()
    
    timeouts = {
        '1': 60000,
        '2': 90000,
        '3': 120000,
        '4': 180000,
        '5': 240000,
    }
    
    if choice == '0':
        print("\n👋 退出测试工具")
        return
    
    elif choice in timeouts:
        test_timeout(timeouts[choice])
    
    elif choice == '6':
        print("\n请输入自定义超时时间（毫秒，范围: 30000-300000）:")
        while True:
            try:
                timeout = int(input("超时时间: ").strip())
                if 30000 <= timeout <= 300000:
                    test_timeout(timeout)
                    break
                else:
                    print("⚠️ 请输入 30000-300000 之间的值")
            except ValueError:
                print("⚠️ 请输入有效的数字")
    
    else:
        print("\n❌ 无效选择")


if __name__ == "__main__":
    main()
