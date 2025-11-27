"""Example API router."""

from fastapi import APIRouter

from app.api.v1.endpoints import example_endpoint

router = APIRouter(prefix="/examples", tags=["Examples"])

# Include all example endpoints
router.include_router(example_endpoint.router)
