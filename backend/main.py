from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from backend.routes import router as webhook_router
except ModuleNotFoundError:
    from routes import router as webhook_router

app = FastAPI(title="GreenCompute AI Agent Engine")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Webhook router
app.include_router(webhook_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "GreenCompute AI Agentic Engine running."}
