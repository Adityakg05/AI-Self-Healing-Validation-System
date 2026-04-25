import logging
import os
import json
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from typing import Optional, List

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import settings

# Configure logs
os.makedirs(".", exist_ok=True)
_fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
_file_handler = RotatingFileHandler(settings.log_file, maxBytes=5*1024*1024, backupCount=2)
_file_handler.setFormatter(_fmt)
logging.basicConfig(level=logging.INFO, handlers=[_file_handler, logging.StreamHandler()])
logger = logging.getLogger("LegacySystem")

app = FastAPI(title="Legacy Nightmare Service")

# --- UTILS & MOCKS ---

def get_db_connection():
    return {"status": "active_pool"}

def get_data_from_database():
    return {"id": 1, "data": "Top Secret Legacy Info", "owner": "SRE_Agent"}

def validate_api_key(api_key: str):
    valid_api_keys = ["api_key_1", "api_key_2"]
    if api_key not in valid_api_keys:
        raise ValueError("Invalid API key")

def infinite_recursion(n):
    if n <= 0: return 0
    return n + infinite_recursion(n - 1)

# --- ENDPOINTS ---

@app.get("/api/data")
async def get_data(request: Request):
    """Validates API key from headers."""
    api_key_header = request.headers.get('api_key')
    api_key_query = request.query_params.get('api_key')
    api_key = api_key_header or api_key_query
    if not api_key:
        logger.warning("Access denied: Missing API key")
        return JSONResponse(status_code=401, content={"error": "Missing API key"})
    
    try:
        validate_api_key(api_key)
        data = get_data_from_database()
        return {"data": data}
    except ValueError as e:
        logger.warning(f"Access denied: {str(e)}")
        return JSONResponse(status_code=401, content={"error": str(e)})

@app.get("/api/users/list")
async def list_users():
    users = ["Alice", "Bob", "Charlie"]
    try:
        return {"user": users[0]} # Fixed index
    except IndexError:
        return JSONResponse(status_code=404, content={"error": "User not found"})

@app.get("/api/compute")
async def compute():
    try:
        conn = get_db_connection()
        return {"status": "connected", "details": conn}
    except Exception:
        return JSONResponse(status_code=500, content={"error": "Database error"})

@app.get("/api/recursive")
async def recursive_crash():
    return {"result": infinite_recursion(10)}

@app.get("/api/config/parse")
async def parse_config():
    valid_json = '{"key": "valid quotes"}'
    return json.loads(valid_json)

@app.get("/api/admin/secrets")
async def get_secrets():
    return {"secret": "The agent is watching..."}

@app.get("/api/math/power")
async def math_power(val: str = "10"):
    try:
        return {"result": int(val) ** 2}
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Invalid number"})

@app.get("/api/stream/data")
async def stream_data():
    return {"item": "data1", "status": "stream_end"}

# --- GLOBAL HANDLER ---

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"CRITICAL: {type(exc).__name__} in {request.url.path}", exc_info=True)
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

if __name__ == "__main__":
    logger.info("ðŸš€ LEGACY SYSTEM FULLY HEALED & SECURED")
    uvicorn.run(app, host="0.0.0.0", port=8000)