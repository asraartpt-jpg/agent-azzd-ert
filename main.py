import sys
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Agentic AI Research Paper System",
    description="Backend API for the multi-agent academic research assistant.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

error_msg = "No error"

try:
    from api.routes import router
    app.include_router(router, prefix="/api/v1")
except Exception as e:
    error_msg = traceback.format_exc()

@app.get("/api/v1/")
async def root():
    if error_msg != "No error":
        return JSONResponse(status_code=500, content={"error": error_msg})
    return {"message": "Welcome to the Agentic AI Research Paper System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
