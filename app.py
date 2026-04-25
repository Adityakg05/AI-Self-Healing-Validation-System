import logging
import os
import uvicorn
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from config import settings

# Setup Logging
_fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
_handler = logging.FileHandler(settings.log_file)
_handler.setFormatter(_fmt)
logging.basicConfig(level=logging.INFO, handlers=[_handler, logging.StreamHandler()])
logger = logging.getLogger("ProductionService")

app = FastAPI(title="AI Self-Healing System")

@app.get("/")
def home():
    return RedirectResponse(url="/docs")

@app.get("/test")
def test():
    return {"status": "working"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run-agent")
def trigger_agent():
    """
    Manually trigger the self-healing agent workflow via API.
    """
    try:
        from main import run_self_healing_workflow
        
        logger.info("Self-healing agent triggered via /run-agent endpoint")
        result = run_self_healing_workflow()
        
        if "error" in result:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Workflow execution failed",
                    "error": result["error"]
                }
            )
            
        return {
            "status": "completed",
            "message": "Self-healing process executed successfully",
            "details": {
                "root_cause_found": result.get("root_cause_identified", False),
                "fix_validated": result.get("fix_validated", False),
                "iterations": result.get("iteration_count", 0),
                "pr_url": result.get("pr_url", "N/A")
            }
        }
    except Exception as e:
        logger.error(f"Error triggering agent: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "An unexpected error occurred",
                "error": str(e)
            }
        )

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
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)