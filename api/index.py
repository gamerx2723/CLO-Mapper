"""
Vercel Serverless Entrypoint for FastAPI Application
"""

import sys
import os
import traceback

# Add project root and current dir to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

try:
    from backend.app import app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    err_msg = str(e)
    tb_msg = traceback.format_exc()
    print(f"FATAL INITIALIZATION ERROR: {err_msg}\n{tb_msg}")

    app = FastAPI()

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    def catch_all(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "status": "initialization_failed",
                "error": err_msg,
                "traceback": tb_msg,
                "sys_path": sys.path[:5],
                "cwd": os.getcwd()
            }
        )
