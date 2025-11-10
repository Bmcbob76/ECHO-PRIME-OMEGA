#!/usr/bin/env python3
"""TRAINERS_GATEWAY HTTP Server"""

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="TRAINERS_GATEWAY")

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9410)
