#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_imports():
    errors = []
    
    print("Checking module imports...")
    print("-" * 60)
    
    try:
        print("✓ Importing backend.app.extensions.db")
        from backend.app.extensions.db import get_conn, put_conn, init_db
    except Exception as e:
        errors.append(f"✗ backend.app.extensions.db: {e}")
    
    try:
        print("✓ Importing backend.app.services.auth")
        from backend.app.services.auth import generate_token, verify_token
    except Exception as e:
        errors.append(f"✗ backend.app.services.auth: {e}")
    
    try:
        print("✓ Importing backend.app.utils.response")
        from backend.app.utils.response import ok, bad_request, unauthorized
    except Exception as e:
        errors.append(f"✗ backend.app.utils.response: {e}")
    
    try:
        print("✓ Importing backend.app.repositories.cities")
        from backend.app.repositories import cities
    except Exception as e:
        errors.append(f"✗ backend.app.repositories.cities: {e}")
    
    try:
        print("✓ Importing backend.app.repositories.air_quality")
        from backend.app.repositories import air_quality
    except Exception as e:
        errors.append(f"✗ backend.app.repositories.air_quality: {e}")
    
    try:
        print("✓ Importing backend.app.repositories.sync_logs")
        from backend.app.repositories import sync_logs
    except Exception as e:
        errors.append(f"✗ backend.app.repositories.sync_logs: {e}")
    
    try:
        print("✓ Importing backend.app.repositories.analytics")
        from backend.app.repositories import analytics
    except Exception as e:
        errors.append(f"✗ backend.app.repositories.analytics: {e}")
    
    try:
        print("✓ Importing backend.app.api.data")
        from backend.app.api.data import bp as data_bp
    except Exception as e:
        errors.append(f"✗ backend.app.api.data: {e}")
    
    try:
        print("✓ Importing backend.app.api.admin")
        from backend.app.api.admin import bp as admin_bp
    except Exception as e:
        errors.append(f"✗ backend.app.api.admin: {e}")
    
    try:
        print("✓ Importing backend.app.tasks.scheduler")
        from backend.app.tasks.scheduler import init_scheduler
    except Exception as e:
        errors.append(f"✗ backend.app.tasks.scheduler: {e}")
    
    try:
        print("✓ Importing backend.app.services.aqicn")
        from backend.app.services.aqicn import sync_air_quality_data
    except Exception as e:
        errors.append(f"✗ backend.app.services.aqicn: {e}")
    
    try:
        print("✓ Creating Flask app")
        from backend.app import create_app
        app = create_app()
    except Exception as e:
        errors.append(f"✗ Flask app: {e}")
    
    print("-" * 60)
    
    if errors:
        print(f"\n❌ Found {len(errors)} errors:\n")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("\n✅ All modules imported successfully!")
        return True

if __name__ == "__main__":
    success = check_imports()
    sys.exit(0 if success else 1)
