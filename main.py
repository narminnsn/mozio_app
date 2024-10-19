from fastapi import FastAPI
from main_app.config import settings
from main_app.routers import provider, service_area
from fastapi_cache import FastAPICache
from redis import Redis

app = FastAPI()

# CORS middleware configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include routers
app.include_router(provider.router)
app.include_router(service_area.router)
