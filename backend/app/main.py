import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.endpoints import router as api_router

app = FastAPI(
    title="Autonomous Cloud IAM Least-Privilege Mitigator",
    description="Autonomous Agentic Security System for Reducing Cloud IAM Permissions while preserving 100% service functionality.",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "title": "Autonomous Cloud IAM Least-Privilege Mitigator API",
        "status": "online",
        "documentation": "/docs",
        "notice": "SYNTHETIC CLOUD ENVIRONMENT — NO PRODUCTION ACCESS REQUIRED OR USED"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=True)
