import logging
import os
import uvicorn
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from config import settings

# Setup logging
_fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
_handler = logging.FileHandler(settings.log_file)
_handler.setFormatter(_fmt)
logging.basicConfig(level=logging.INFO, handlers=[_handler, logging.StreamHandler()])
logger = logging.getLogger("ProductionService")

app = FastAPI(title="AI-Self-Healing-Validation-System")

@app.get("/")
def home():
    return RedirectResponse(url="/docs")

@app.get("/test")
def test():
    # Basic connectivity check
    return {"status": "working"}

@app.get("/health")
def health():
    # Enhanced readiness probe for monitoring systems
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "AI-Self-Healing-Validation-System",
        "version": "1.0.0",
        "uptime": "active"
    }

@app.get("/ping")
def ping():
    # Simple ping endpoint for keep-alive services
    return {"message": "pong", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.post("/run-agent")
def trigger_agent():
    """Trigger self-healing agent workflow."""
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
    """FastAPI app with intentional bug for SRE agent demo."""
    # Log incoming requests for debugging
    logger.info(f"Endpoint called. TriggerBug={x_trigger_bug}")
    
    user_config = {
        "user_id": 12345,
        "username": "demo_user",
        "roles": ["admin", "developer"]
    }

    if x_trigger_bug and x_trigger_bug.lower() == "true":
        logger.warning("Simulating crash...")
        # INTENTIONAL BUG
        api_key = user_config["api_key"] 
        return {"data": {"key": api_key}, "message": "Success", "timestamp": "now"}

    return DataResponse(
        data=user_config,
        message="Success",
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@app.get("/api/logs")
def get_logs():
    """Retrieve application logs."""
    try:
        if os.path.exists(settings.log_file):
            with open(settings.log_file, "r") as f:
                logs = f.read()
            return {"logs": logs, "status": "success"}
        else:
            return {"logs": "", "status": "not_found", "message": "Log file not found"}
    except Exception as e:
        return {"logs": "", "status": "error", "message": str(e)}

@app.exception_handler(Exception)
async def handle_crash(request: Request, exc: Exception):
    logger.error(f"CRITICAL ERROR in {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)