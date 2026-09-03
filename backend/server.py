from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import os
import logging
from pathlib import Path
from urllib.parse import urlsplit
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from database import engine
from routers import auth, habits, leaderboard


# Startup runs before the yield, shutdown after it. Add your own setup/teardown here.
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


# Create the main app without a prefix
app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def enforce_allowed_origins(request: Request, call_next):
    origin = request.headers.get("origin")
    public_origins = set(os.environ["CORS_ORIGINS"].split(","))
    ingress_origins = set(filter(None, os.environ.get("TRUSTED_INGRESS_ORIGINS", "").split(",")))
    fetch_site = request.headers.get("sec-fetch-site")
    referer = request.headers.get("referer")
    referer_origin = None
    if referer:
        parsed = urlsplit(referer)
        referer_origin = f"{parsed.scheme}://{parsed.netloc}"
        blocked_cross_site = referer_origin and referer_origin not in public_origins
        blocked_origin = origin and origin not in public_origins and origin not in ingress_origins
    if blocked_cross_site or blocked_origin:
        return JSONResponse(status_code=403, content={"detail": "Origin not allowed"})
    return await call_next(request)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Smart Habit Tracker API", "status": "ok"}


api_router.include_router(auth.router)
api_router.include_router(habits.router)
api_router.include_router(leaderboard.router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Include the router in the main app last so every endpoint stays under /api.
app.include_router(api_router)
