from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.schemas import TranslationParameters
from app.hardware_detector import get_hardware_info
from app.compute_manager import ComputeManager

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="On-Demand AI Compute Engine",
    description="A dynamic AI execution engine using remote compute providers.",
    version="1.0.0",
)

from fastapi.staticfiles import StaticFiles
from pathlib import Path

frontend_path = Path(__file__).resolve().parent.parent / "frontend"

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

frontend_path = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/")
async def frontend():
    return FileResponse(frontend_path / "index.html")


# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Request schema
class ComputeRequest(BaseModel):
    task: str
    parameters: dict = Field(default_factory=dict)


class ComputeResponse(BaseModel):
    status: str
    task: str
    provider: str
    result: str


# Initialize compute manager
compute_manager = ComputeManager()


# Root endpoint
@app.get("/")
async def root():
    return {
        "project": "On-Demand AI Compute Engine",
        "status": "running",
        "message": "Welcome to the AI Compute Engine!",
    }


# Backend health
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "On-Demand AI Compute Engine",
        "inference_mode": "remote",
    }


# Provider readiness and hardware information
@app.get("/compute/status")
async def compute_status():

    provider = compute_manager.registry.get_provider("translation")
    provider_configured = provider.is_available()

    return {
        "status": "available" if provider_configured else "unavailable",
        "backend": "running",
        "recommended_compute": "REMOTE",
        "inference_provider": provider.name,
        "provider_configured": provider_configured,
        "hardware": get_hardware_info(),
    }


# Supported tasks
@app.get("/compute/tasks")
async def get_supported_tasks():

    tasks = compute_manager.get_supported_tasks()

    return {"supported_tasks": tasks, "total": len(tasks)}


# Execute AI task
@app.post("/compute/execute", response_model=ComputeResponse)
@limiter.limit("5/minute")
def execute_compute(request: Request, payload: ComputeRequest):

    try:

        if payload.task == "translation":

            parameters = TranslationParameters.model_validate(payload.parameters)

            validated_parameters = parameters.model_dump()

        else:

            compute_manager.registry.get_provider(payload.task)

            validated_parameters = payload.parameters

        result = compute_manager.execute(task=payload.task, **validated_parameters)

        return result

    except ValidationError as error:

        raise HTTPException(status_code=422, detail=error.errors())

    except ValueError as error:

        raise HTTPException(status_code=400, detail=str(error))

    except RuntimeError:

        raise HTTPException(
            status_code=502,
            detail="The remote AI provider is temporarily unavailable. Please try again later.",
        )
