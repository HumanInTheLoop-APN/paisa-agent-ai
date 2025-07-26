#!/usr/bin/env python3
"""
Run script for the Talk to Your Money Backend
"""

import os

import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "false").lower() == "true"

    print(f"Starting Talk to Your Money Backend on {host}:{port}")
    print(f"Debug mode: {reload}")
    print(f"API Documentation: http://{host}:{port}/docs")

    uvicorn.run("src.main:app", host=host, port=port, reload=reload, log_level="info")
