import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from backend.app.services.aqicn import sync_air_quality_data

scheduler = None

def init_scheduler():
    global scheduler
    
    if scheduler is not None and scheduler.running:
        return
    
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(
        func=sync_air_quality_data,
        trigger='interval',
        hours=1,
        id='sync_air_quality',
        name='Sync air quality data from AQICN',
        replace_existing=True
    )
    
    scheduler.start()

def stop_scheduler():
    global scheduler
    
    if scheduler is not None and scheduler.running:
        scheduler.shutdown()
        scheduler = None

def get_scheduler():
    return scheduler
