from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.errors import VaporException, ErrorCode
from app.middleware.request_logging import RequestLoggingMiddleware
from app.api.routers import health, auth, workspace, home, missions, memories, content, deliverables, attention, search, integrations

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Standardized Exception Handler for VaporException
@app.exception_handler(VaporException)
async def vapor_exception_handler(request: Request, exc: VaporException):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "request_id": request_id,
            "path": str(request.url.path),
            "details": exc.details
        }
    )

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": ErrorCode.INTERNAL_ERROR,
            "message": "An unexpected error occurred on the Vapor core API.",
            "request_id": request_id,
            "path": str(request.url.path)
        }
    )

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
app.include_router(workspace.router, prefix=settings.API_V1_STR, tags=["Workspace"])
app.include_router(home.router, prefix=settings.API_V1_STR, tags=["Home"])
app.include_router(missions.router, prefix=settings.API_V1_STR, tags=["Missions"])
app.include_router(memories.router, prefix=settings.API_V1_STR, tags=["Memories"])
app.include_router(content.router, prefix=settings.API_V1_STR, tags=["Content"])
app.include_router(deliverables.router, prefix=settings.API_V1_STR, tags=["Deliverables"])
app.include_router(attention.router, prefix=settings.API_V1_STR, tags=["Attention"])
app.include_router(search.router, prefix=settings.API_V1_STR, tags=["Search"])
app.include_router(integrations.router, prefix=settings.API_V1_STR, tags=["Integrations"])

@app.get("/")
async def root():
    return {
        "message": "Vapor OS Core Kernel API",
        "docs": f"{settings.API_V1_STR}/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
