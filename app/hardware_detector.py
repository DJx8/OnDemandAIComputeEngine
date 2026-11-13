import platform
import psutil
import torch


def get_cpu_info():
    """Collect CPU information."""

    return {
        "name": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
    }


def get_memory_info():
    """Collect system memory information."""

    memory = psutil.virtual_memory()

    return {
        "total_gb": round(memory.total / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "used_percent": memory.percent,
    }


def get_gpu_info():
    """Detect NVIDIA CUDA GPU availability."""

    if not torch.cuda.is_available():
        return {
            "available": False,
            "name": None,
            "memory_total_gb": None,
            "memory_free_gb": None,
        }

    gpu = torch.cuda.get_device_properties(0)

    free_memory, total_memory = torch.cuda.mem_get_info(0)

    return {
        "available": True,
        "name": gpu.name,
        "memory_total_gb": round(total_memory / (1024**3), 2),
        "memory_free_gb": round(free_memory / (1024**3), 2),
    }


def get_hardware_info():
    """Collect all hardware information."""

    return {"cpu": get_cpu_info(), "memory": get_memory_info(), "gpu": get_gpu_info()}
