#!/usr/bin/env python
"""
空气质量监测系统 - 完整数据导入脚本
支持从 AQICN API 导入空气质量数据
"""

import sys
import os
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from backend.app.repositories import cities, air_quality
from backend.app.services.aqicn import sync_air_quality_data
from datetime import datetime
import time

def import_cities():
    """导入城市数据"""
    print("\n[第一步] 导入城市数据...")
    print("-" * 60)
    
    city_data = [
        ('Beijing', 'Beijing', 39.9042, 116.4074),
    ]
    
    created = 0
    skipped = 0
    
    for name, province, lat, lon in city_data:
        try:
            city, err = cities.create_city(name, province, lat, lon)
            if err == 'exists':
                print(f"  ⊘ {name:8} ({province:8}) - 已存在")
                skipped += 1
            else:
                print(f"  ✓ {name:8} ({province:8}) - 已添加")
                created += 1
        except Exception as e:
            print(f"  ✗ {name:8} ({province:8}) - 错误: {e}")
    
    print("-" * 60)
    print(f"导入结果: 成功 {created}，跳过 {skipped}")
    return created + skipped

def sync_air_quality():
    """同步空气质量数据"""
    print("\n[第二步] 同步空气质量数据...")
    print("-" * 60)
    print("正在从 AQICN API 获取数据...")
    print("（这可能需要几分钟，请耐心等待）")
    
    try:
        start_time = time.time()
        sync_air_quality_data()
        elapsed = time.time() - start_time
        
        print("-" * 60)
        print(f"✓ 同步完成 (耗时: {elapsed:.1f}秒)")
        return True
    except Exception as e:
        print("-" * 60)
        print(f"✗ 同步失败: {e}")
        print("\n可能的原因:")
        print("  1. AQICN API Token 无效或过期")
        print("  2. 网络连接问题")
        print("  3. 没有城市数据")
        print("\n解决方案:")
        print("  - 检查 .env 文件中的 AQICN_API_TOKEN")
        print("  - 确保网络连接正常")
        print("  - 先运行第一步导入城市数据")
        return False

def verify_data():
    """验证导入的数据"""
    print("\n[第三步] 验证导入的数据...")
    print("-" * 60)
    
    try:
        # 获取城市总数
        all_cities, total, _ = cities.get_all_cities(page=1, page_size=100)
        print(f"城市总数: {total}")
        
        if not all_cities:
            print("警告: 没有城市数据！")
            return False
        
        # 检查每个城市的数据
        print("\n城市空气质量数据状态:")
        print("-" * 60)
        
        cities_with_data = 0
        cities_without_data = 0
        
        for city in all_cities:
            data = air_quality.get_latest_air_quality(city['id'])
            if data:
                aqi = data.get('aqi', 'N/A')
                level = data.get('aqi_level', 'N/A')
                recorded = data.get('recorded_time', 'N/A')
                print(f"  ✓ {city['name']:10} - AQI: {aqi:3} ({level:8}) @ {recorded}")
                cities_with_data += 1
            else:
                print(f"  ⊘ {city['name']:10} - 无数据")
                cities_without_data += 1
        
        print("-" * 60)
        print(f"有数据: {cities_with_data}, 无数据: {cities_without_data}")
        
        return cities_with_data > 0
    except Exception as e:
        print(f"✗ 验证失败: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("🌍 空气质量监测系统 - 数据导入工具")
    print("=" * 60)
    
    # 确保数据库连接
    try:
        from backend.app.extensions.db import init_db
        init_db()
        print("\n✓ 数据库连接成功")
    except Exception as e:
        print(f"\n✗ 数据库连接失败: {e}")
        return
    
    # 步骤 1: 导入城市
    city_count = import_cities()
    
    # 步骤 2: 同步数据
    sync_ok = sync_air_quality()
    
    # 步骤 3: 验证数据
    verify_ok = verify_data()
    
    # 最终结果
    print("\n" + "=" * 60)
    print("📊 导入完成总结")
    print("=" * 60)
    
    if city_count > 0 and sync_ok and verify_ok:
        print("\n✅ 数据导入成功！")
        print("\n接下来可以：")
        print("  1. 访问 API 查询数据:")
        print("     - 查看城市: GET /data/cities")
        print("     - 查询数据: GET /data/query?city_id=1")
        print("     - 月度统计: GET /data/monthly-stats?city_id=1")
        print("\n  2. 查看同步日志:")
        print("     - GET /admin/data/sync-logs")
        print("\n  3. 设置定时同步:")
        print("     - 系统已配置每小时自动同步一次")
    else:
        print("\n⚠️  部分步骤未完成，请检查上面的错误信息")
    
    print("\n需要帮助? 查看: DATA_IMPORT_GUIDE.md")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        print(f"\n\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
