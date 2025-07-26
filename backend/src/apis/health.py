from fastapi import APIRouter, HTTPException

from ..services.runner_manager_service import RunnerManagerService

router = APIRouter()
runner_manager_service = RunnerManagerService()


@router.get("/healthz")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "Talk to Your Money Backend",
        "version": "1.0.0",
    }


@router.get("/readiness")
async def readiness_check():
    """Readiness check endpoint for Kubernetes"""
    try:
        # Check runner manager health
        runner_health = await runner_manager_service.health_check()

        return {
            "status": "ready",
            "service": "Talk to Your Money Backend",
            "version": "1.0.0",
            "components": {"runner_manager": runner_health},
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service not ready: {str(e)}")


@router.get("/liveness")
async def liveness_check():
    """Liveness check endpoint for Kubernetes"""
    return {"status": "alive", "service": "Talk to Your Money Backend"}
