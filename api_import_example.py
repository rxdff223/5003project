#!/usr/bin/env python
"""
空气质量监测系统 - API 数据导入示例
演示如何通过 API 导入和查询数据
"""

import requests
import json
from datetime import datetime
import time

BASE_URL = 'http://127.0.0.1:5000'

class APIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.user_id = None
    
    def register(self, phone, password, nickname):
        """用户注册"""
        response = self.session.post(
            f"{self.base_url}/auth/register",
            json={"phone": phone, "password": password, "nickname": nickname}
        )
        return response.json()
    
    def login(self, phone, password):
        """用户登录"""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"phone": phone, "password": password}
        )
        data = response.json()
        if data.get('code') == 'success':
            self.token = data['data'].get('token')
            self.user_id = data['data']['user'].get('id')
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
        return data
    
    def get_cities(self, page=1, page_size=20, query=''):
        """获取城市列表"""
        response = self.session.get(
            f"{self.base_url}/data/cities",
            params={'page': page, 'page_size': page_size, 'q': query}
        )
        return response.json()
    
    def get_city_detail(self, city_id):
        """获取城市详情"""
        response = self.session.get(
            f"{self.base_url}/data/cities/{city_id}"
        )
        return response.json()
    
    def get_latest_data(self, city_id):
        """获取最新空气质量数据"""
        response = self.session.get(
            f"{self.base_url}/data/detail",
            params={'city_id': city_id}
        )
        return response.json()
    
    def query_air_quality(self, city_id, page=1, page_size=20):
        """查询空气质量历史数据"""
        response = self.session.get(
            f"{self.base_url}/data/query",
            params={'city_id': city_id, 'page': page, 'page_size': page_size}
        )
        return response.json()
    
    def get_monthly_stats(self, city_id, months=12):
        """获取月度统计"""
        response = self.session.get(
            f"{self.base_url}/data/monthly-stats",
            params={'city_id': city_id, 'months': months}
        )
        return response.json()

def main():
    print("\n" + "=" * 70)
    print("🌍 空气质量监测系统 - API 使用示例")
    print("=" * 70)
    
    client = APIClient()
    
    # 步骤 1: 用户注册
    print("\n[1️⃣  步骤] 用户注册")
    print("-" * 70)
    
    phone = f"138001380{int(time.time()) % 100:02d}"
    print(f"注册用户: {phone}")
    
    result = client.register(phone, "password123", "TestUser")
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if result.get('code') != 'created':
        print("✗ 注册失败!")
        return
    
    # 步骤 2: 用户登录
    print("\n[2️⃣  步骤] 用户登录")
    print("-" * 70)
    
    result = client.login(phone, "password123")
    print(f"✓ 登录成功")
    print(f"Token: {client.token[:50]}...")
    
    # 步骤 3: 查询城市列表
    print("\n[3️⃣  步骤] 查询城市列表")
    print("-" * 70)
    
    result = client.get_cities(page=1, page_size=10)
    print(f"响应状态: {result.get('code')}")
    
    cities = result.get('data', {}).get('items', [])
    if cities:
        print(f"查询到 {result['data']['total']} 个城市，显示前 10 个:")
        for city in cities[:10]:
            print(f"  - {city['name']:10} ({city['province']:8}) @ ({city['lat']}, {city['lon']})")
        
        test_city_id = cities[0]['id']
        test_city_name = cities[0]['name']
    else:
        print("⚠️  没有城市数据！请先运行 import_data.py 导入城市数据")
        return
    
    # 步骤 4: 获取城市详情
    print(f"\n[4️⃣  步骤] 获取城市详情 ({test_city_name})")
    print("-" * 70)
    
    result = client.get_city_detail(test_city_id)
    if result.get('code') == 'success':
        city = result['data']
        print(f"✓ 获取成功:")
        print(f"  城市名: {city['name']}")
        print(f"  省份: {city['province']}")
        print(f"  坐标: ({city['lat']}, {city['lon']})")
    
    # 步骤 5: 获取最新空气质量数据
    print(f"\n[5️⃣  步骤] 获取最新空气质量数据 ({test_city_name})")
    print("-" * 70)
    
    result = client.get_latest_data(test_city_id)
    if result.get('code') == 'success':
        data = result['data'].get('latest_data')
        if data:
            print(f"✓ 获取成功:")
            print(f"  AQI: {data.get('aqi')}")
            print(f"  等级: {data.get('aqi_level')}")
            print(f"  主要污染物: {data.get('dominant_pol')}")
            print(f"  PM2.5: {data.get('pm25')} μg/m³")
            print(f"  PM10: {data.get('pm10')} μg/m³")
            print(f"  O3: {data.get('o3')} ppb")
            print(f"  NO2: {data.get('no2')} ppb")
            print(f"  SO2: {data.get('so2')} ppb")
            print(f"  CO: {data.get('co')} ppm")
            print(f"  记录时间: {data.get('recorded_time')}")
        else:
            print("⚠️  没有空气质量数据！请先运行 import_data.py 同步数据")
    else:
        print(f"✗ 获取失败: {result.get('message')}")
    
    # 步骤 6: 查询历史数据
    print(f"\n[6️⃣  步骤] 查询历史空气质量数据 ({test_city_name})")
    print("-" * 70)
    
    result = client.query_air_quality(test_city_id, page=1, page_size=5)
    if result.get('code') == 'success':
        items = result['data'].get('items', [])
        total = result['data'].get('total', 0)
        print(f"✓ 查询成功 (总计 {total} 条记录, 显示前 5 条):")
        for item in items:
            print(f"  - {item['recorded_time']} AQI {item['aqi']} ({item['aqi_level']})")
    else:
        print(f"✗ 查询失败: {result.get('message')}")
    
    # 步骤 7: 获取月度统计
    print(f"\n[7️⃣  步骤] 获取月度统计 ({test_city_name})")
    print("-" * 70)
    
    result = client.get_monthly_stats(test_city_id, months=6)
    if result.get('code') == 'success':
        stats = result['data'].get('monthly_stats', [])
        print(f"✓ 查询成功 (近 6 个月):")
        for stat in stats:
            print(f"  - {stat['month']} 好天数占比: {stat['good_ratio']*100:.1f}% PM2.5平均: {stat['pm25_avg']}")
    else:
        print(f"✗ 查询失败: {result.get('message')}")
    
    print("\n" + "=" * 70)
    print("✅ 演示完成！")
    print("=" * 70)
    print("\n📚 详细信息请查看: DATA_IMPORT_GUIDE.md")
    print()

if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器！")
        print("请确保 Flask 应用已启动: python run.py --port 5000")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
