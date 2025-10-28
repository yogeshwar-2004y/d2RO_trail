#!/usr/bin/env python3
"""
Backend server startup script
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("Starting AVIATRAX Backend Server...")
    print("Server will be available at: http://localhost:8000")
    print("API endpoints available at: http://localhost:8000/api")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=8000)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
