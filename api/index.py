from http.server import BaseHTTPRequestHandler
import sys
import os
import json
import traceback

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        info = {
            "status": "diagnostic",
            "python_version": sys.version,
            "cwd": os.getcwd(),
            "files": os.listdir(os.getcwd()) if os.path.exists(os.getcwd()) else []
        }

        try:
            api_dir = os.path.dirname(os.path.abspath(__file__))
            if api_dir not in sys.path:
                sys.path.insert(0, api_dir)
            from backend.app import app
            info["backend_app"] = "SUCCESS"
        except Exception as e:
            info["backend_app_error"] = str(e)
            info["traceback"] = traceback.format_exc()

        self.wfile.write(json.dumps(info, indent=2).encode('utf-8'))
