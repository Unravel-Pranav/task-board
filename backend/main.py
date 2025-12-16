"""Main FastAPI Application - Task Board API."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.routers.task_router import router as task_router

# Create FastAPI app
app = FastAPI(
    title="Task Board API",
    description="A clean, full-stack task management application",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(task_router, prefix="/api")


# Health check endpoint
@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "message": "Task Board API is running!"}


# Serve static files (frontend build)
frontend_path = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_path.exists():
    app.mount("/assets", StaticFiles(directory=frontend_path / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str) -> FileResponse:
        """Serve frontend files."""
        file_path = frontend_path / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(frontend_path / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

