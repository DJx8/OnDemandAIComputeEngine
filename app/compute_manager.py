from app.provider_registry import ProviderRegistry
from providers.huggingface_space import HuggingFaceSpaceProvider


class ComputeManager:

    def __init__(self):

        self.registry = ProviderRegistry()

        # Register available providers.
        self.registry.register(HuggingFaceSpaceProvider())

    def execute(self, task: str, **kwargs):

        # Find the provider responsible for this task.
        provider = self.registry.get_provider(task)

        # Execute the requested task.
        result = provider.execute(task=task, **kwargs)

        return {
            "status": "success",
            "task": task,
            "provider": provider.name,
            "result": result,
        }

    def get_supported_tasks(self):

        return self.registry.get_supported_tasks()
