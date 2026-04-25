import logging
import os
import json
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from typing import Optional, List

import uvicorn
from fastapi import FastAPI, Request, Depends
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

# --- UTILS WITH HIDDEN BUGS ---

def get_db_connection():
    # Fix: Define the connection pool and active connection
    connection_pool = {}  # Initialize an empty connection pool
    active_connection = None  # Initialize active connection to None
    return active_connection  # Return the active connection

def infinite_recursion(n):
    # Fix: Add a base case to prevent infinite recursion
    if n <= 0:
        return n
    return infinite_recursion(n - 1)

# --- ENDPOINTS ---

@app.get("/api/users/list")
async def list_users():
    """Fix: Handle IndexError by returning a 404 response."""
    users = ["Alice", "Bob", "Charlie"]
    try:
        logger.info("Fetching user at index 999...")
        return {"user": users[999]}
    except IndexError:
        return {"error": "User not found"}, 404

@app.get("/api/compute")
async def compute():
    """Fix: Handle NameError by returning a 500 response."""
    logger.info("Starting quantum computation...")
    try:
        conn = get_db_connection()
        return {"status": "connected"}
    except Exception as e:
        logger.error(f"Computation failed: {e}")
        return {"error": "Internal Server Error"}, 500

@app.get("/api/recursive")
async def recursive_crash():
    """Fix: Handle RecursionError by returning a 500 response."""
    logger.info("Entering the void...")
    try:
        return {"result": infinite_recursion(1)}
    except RecursionError:
        return {"error": "Internal Server Error"}, 500

@app.get("/api/config/parse")
async def parse_config():
    """Fix: Handle JSONDecodeError by returning a 400 response."""
    bad_json = "{ 'key': 'missing quotes' }"
    try:
        logger.info("Parsing legacy config...")
        return json.loads(bad_json)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON configuration"}, 400

@app.get("/api/admin/secrets")
async def get_secrets():
    """Fix: Handle FileNotFoundError by returning a 404 response."""
    logger.info("Accessing forbidden secrets...")
    try:
        with open("vault/secrets.txt", "r") as f:
            return {"secret": f.read()}
    except FileNotFoundError:
        return {"error": "Secrets not found"}, 404

@app.get("/api/math/power")
async def math_power(val: str = "oops"):
    """Fix: Handle ValueError by returning a 400 response."""
    logger.info(f"Calculating power of {val}...")
    try:
        return {"result": int(val) ** 2}
    except ValueError:
        return {"error": "Invalid input: Expected a number"}, 400

@app.get("/api/stream/data")
async def stream_data():
    """Fix: Handle StopIteration by returning a 404 response."""
    def simple_gen():
        yield "data1"
    
    g = simple_gen()
    try:
        next(g)
        logger.info("Attempting to pull from exhausted generator...")
        return {"item": next(g)}
    except StopIteration:
        return {"error": "No more data available"}, 404

# --- API KEY VALIDATION ---

def validate_api_key(api_key: str):
    # Fix: Validate API key against a known set of values or a database
    valid_api_keys = ["api_key_1", "api_key_2"]  # Replace with actual validation logic
    if api_key not in valid_api_keys:
        raise ValueError("Invalid API key")

# --- ENDPOINTS WITH API KEY VALIDATION ---

@app.get("/api/data")
async def get_data():
    """Fix: Validate API key before proceeding."""
    api_key = request.headers.get('api_key')
    if not api_key:
        return {"error": "Missing API key"}, 401
    try:
        validate_api_key(api_key)
    except ValueError as e:
        return {"error": str(e)}, 401
    # Proceed with the request
    data = get_data_from_database()
    return {"data": data}

# --- CATCH-ALL EXCEPTION HANDLER FOR THE AGENT ---

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"CRITICAL SYSTEM FAILURE in {request.url.path}: {type(exc).__name__} - {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "CRITICAL_ERROR", "type": type(exc).__name__, "msg": str(exc)}
    )

if __name__ == "__main__":
    logger.info("ðŸš€ LEGACY NIGHTMARE HEALED on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)