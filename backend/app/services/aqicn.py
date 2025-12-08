import os
import requests
from datetime import datetime
from backend.app.repositories import cities, air_quality, sync_logs

AQICN_API_TOKEN = os.getenv('AQICN_API_TOKEN', '2e1b5d79c4b27bfebf99f213f77c70985b32d52f')
AQICN_BASE_URL = 'http://api.waqi.info'

def sync_air_quality_data(sync_log_id=None):
    if not sync_log_id:
        sync_log_id, _ = sync_logs.log_sync(
            sync_type='scheduled',
            data_source='AQICN',
            start_time=datetime.utcnow(),
            status='in_progress'
        )
    
    success_count = 0
    fail_count = 0
    error_message = None
    
    try:
        all_cities, _, _ = cities.get_all_cities(page=1, page_size=1000)
        
        if not all_cities:
            error_message = "no_cities_found"
            sync_logs.update_sync_log(
                sync_log_id,
                end_time=datetime.utcnow(),
                status='failed',
                success_count=0,
                fail_count=0,
                total_count=0,
                error_message=error_message
            )
            return
        
        for city in all_cities:
            try:
                data = fetch_city_air_quality(city['name'], city['province'])
                if data:
                    data['city_id'] = city['id']
                    air_quality.save_air_quality_data(
                        city_id=data['city_id'],
                        recorded_time=data['recorded_time'],
                        aqi=data.get('aqi'),
                        aqi_level=data.get('aqi_level'),
                        dominant_pol=data.get('dominant_pol'),
                        pm25=data.get('pm25'),
                        pm10=data.get('pm10'),
                        o3=data.get('o3'),
                        no2=data.get('no2'),
                        so2=data.get('so2'),
                        co=data.get('co'),
                        source='AQICN',
                        attribution=data.get('attribution')
                    )
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                fail_count += 1
        
        sync_logs.update_sync_log(
            sync_log_id,
            end_time=datetime.utcnow(),
            status='success',
            success_count=success_count,
            fail_count=fail_count,
            total_count=len(all_cities)
        )
    
    except Exception as e:
        error_message = str(e)
        sync_logs.update_sync_log(
            sync_log_id,
            end_time=datetime.utcnow(),
            status='failed',
            success_count=success_count,
            fail_count=fail_count,
            total_count=fail_count + success_count,
            error_message=error_message
        )

def fetch_city_air_quality(city_name, province=None):
    try:
        query = f"{city_name}"
        if province:
            query = f"{province},{city_name}"
        
        url = f"{AQICN_BASE_URL}/feed/{query}/?token={AQICN_API_TOKEN}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        if data.get('status') != 'ok':
            return None
        
        aqicn_data = data.get('data', {})
        
        aqi_value = aqicn_data.get('aqi')
        aqi_level = get_aqi_level(aqi_value)
        
        result = {
            'recorded_time': datetime.utcnow(),
            'aqi': aqi_value,
            'aqi_level': aqi_level,
            'dominant_pol': aqicn_data.get('dominentpol'),
            'attribution': aqicn_data.get('attributions', [{}])[0].get('name', 'AQICN'),
        }
        
        iaqi = aqicn_data.get('iaqi', {})
        result['pm25'] = iaqi.get('pm25', {}).get('v')
        result['pm10'] = iaqi.get('pm10', {}).get('v')
        result['o3'] = iaqi.get('o3', {}).get('v')
        result['no2'] = iaqi.get('no2', {}).get('v')
        result['so2'] = iaqi.get('so2', {}).get('v')
        result['co'] = iaqi.get('co', {}).get('v')
        
        return result
    
    except Exception as e:
        return None

def get_aqi_level(aqi_value):
    if aqi_value is None:
        return None
    
    aqi_value = int(aqi_value)
    
    if aqi_value <= 50:
        return 'Excellent'
    elif aqi_value <= 100:
        return 'Good'
    elif aqi_value <= 150:
        return 'Light Pollution'
    elif aqi_value <= 200:
        return 'Moderate Pollution'
    elif aqi_value <= 300:
        return 'Heavy Pollution'
    else:
        return 'Severe Pollution'

