#!/usr/bin/env python3
"""
Keep-Alive Service for AI-Self-Healing-Validation-System Backend

This service keeps the FastAPI backend alive by pinging it every 10 minutes.
Run this continuously to prevent Render free tier from sleeping.
"""

import requests
import time
import logging
import os
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KeepAliveService:
    def __init__(self):
        self.backend_url = os.getenv("BACKEND_URL", "https://ai-self-healing-validation-system.onrender.com")
        self.ping_interval = 600  # 10 minutes in seconds
        
    def ping_backend(self):
        """Ping the backend to keep it alive."""
        endpoints = [
            f"{self.backend_url}/health",
            f"{self.backend_url}/ping",
            f"{self.backend_url}/test"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=15)
                if response.status_code == 200:
                    logger.info(f"✅ Successfully pinged {endpoint}")
                    return True
                else:
                    logger.warning(f"⚠️ {endpoint} returned {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Failed to ping {endpoint}: {e}")
        
        return False
    
    def run(self):
        """Run the keep-alive service continuously."""
        logger.info("🚀 Starting Keep-Alive Service...")
        logger.info(f"📍 Backend URL: {self.backend_url}")
        logger.info(f"⏰ Ping interval: {self.ping_interval} seconds")
        
        consecutive_failures = 0
        max_failures = 3
        
        while True:
            try:
                success = self.ping_backend()
                
                if success:
                    consecutive_failures = 0
                    logger.info(f"💚 Backend is alive - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    consecutive_failures += 1
                    logger.warning(f"💔 Backend ping failed {consecutive_failures}/{max_failures} times")
                    
                    if consecutive_failures >= max_failures:
                        logger.error("🚨 Backend appears to be down! Check your deployment.")
                        # Continue trying anyway
                
                # Wait for next ping
                time.sleep(self.ping_interval)
                
            except KeyboardInterrupt:
                logger.info("🛑 Keep-Alive Service stopped by user")
                break
            except Exception as e:
                logger.error(f"💥 Unexpected error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    service = KeepAliveService()
    service.run()
