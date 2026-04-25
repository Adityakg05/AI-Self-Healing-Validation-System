import logging
import os
import uvicorn
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import settings

# Setup Logging
_fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
_handler = logging.FileHandler(settings.log_file)
_handler.setFormatter(_fmt)
logging.basicConfig(level=logging.INFO, handlers=[_handler, logging.StreamHandler()])
logger = logging.getLogger("ProductionService")

app = FastAPI(title="SRE Monitored Service")

class DataResponse(BaseModel):
    data: dict
    message: str
    timestamp: str

@app.get("/api/data", response_model=DataResponse)
async def get_data(
    request: Request,
    x_trigger_bug: Optional[str] = Header(None, alias="X-Trigger-Bug")
):
    """
    Core data endpoint.
    BUG: When X-Trigger-Bug is 'true', it crashes with a KeyError due to 
    accessing a missing 'api_key' in the user_config.
    """
    logger.info(f"Endpoint called. TriggerBug={x_trigger_bug}")
    
    user_config = {
        "user_id": 12345,
        "username": "demo_user",
        "roles": ["admin", "developer"]
    }

    if x_trigger_bug and x_trigger_bug.lower() == "true":
        logger.warning("Simulating crash...")
        # INTENTIONAL BUG FOR SRE AGENT TO FIX
        api_key = user_config["api_key"] 
        return {"data": {"key": api_key}, "message": "Success", "timestamp": "now"}

    return DataResponse(
        data=user_config,
        message="Success",
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@app.exception_handler(Exception)
async def handle_crash(request: Request, exc: Exception):
    logger.error(f"CRITICAL ERROR in {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)