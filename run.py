#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description='Air quality monitoring system backend service')
    parser.add_argument('--production', action='store_true', help='Run in production mode')
    parser.add_argument('--port', type=int, default=5000, help='Service port')
    parser.add_argument('--host', default='0.0.0.0', help='Service host')
    parser.add_argument('--workers', type=int, default=4, help='Gunicorn worker count')
    
    args = parser.parse_args()
    
    os.environ['FLASK_APP'] = 'backend.app:create_app'
    os.environ['FLASK_ENV'] = 'production' if args.production else 'development'
    
    if args.production:
        try:
            from gunicorn.app.wsgiapp import run
            sys.argv = [
                'gunicorn',
                f'--workers={args.workers}',
                f'--bind={args.host}:{args.port}',
                '--timeout=60',
                '--access-logfile=-',
                '--error-logfile=-',
                'backend.app:create_app()'
            ]
            run()
        except ImportError:
            print("Error: gunicorn is not installed")
            print("Please run: pip install gunicorn")
            sys.exit(1)
    else:
        from flask import Flask
        from backend.app import create_app
        
        app = create_app()
        app.run(
            host=args.host,
            port=args.port,
            debug=True,
            use_reloader=False
        )

if __name__ == '__main__':
    main()
