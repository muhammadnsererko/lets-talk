#!/usr/bin/env python3
"""
Production server launcher for Let's Talk API
Supports both development and production modes
"""
import os
import sys
import argparse
from app import app

def main():
    parser = argparse.ArgumentParser(description='Let\'s Talk API Server')
    parser.add_argument('--prod', action='store_true', help='Run in production mode')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ['PORT'] = str(args.port)
    
    if args.prod:
        os.environ['FLASK_ENV'] = 'production'
        print(f"🚀 Starting production server on {args.host}:{args.port}")
        
        try:
            from waitress import serve
            serve(app, host=args.host, port=args.port)
        except ImportError:
            print("❌ waitress not installed. Install with: pip install waitress")
            print("💡 Falling back to Flask development server...")
            app.run(host=args.host, port=args.port, debug=False)
    else:
        os.environ['FLASK_ENV'] = 'development'
        print(f"🛠️ Starting development server on {args.host}:{args.port}")
        app.run(host=args.host, port=args.port, debug=True)

if __name__ == '__main__':
    main()