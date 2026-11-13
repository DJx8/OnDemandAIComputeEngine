class ProviderRegistry:

    def __init__(self):
        self.providers = {}

    def register(self, provider):

        supported_tasks = provider.SUPPORTED_TASKS

        if not supported_tasks:
            raise ValueError(f"Provider {provider.name} has no supported tasks.")

        # Check for duplicate task registrations.
        for task in supported_tasks:
            if task in self.providers:
                raise ValueError(f"Task '{task}' is already registered.")

        # Register the provider for each supported task.
        for task in supported_tasks:
            self.providers[task] = provider

    def get_provider(self, task: str):

        provider = self.providers.get(task)

        if provider is None:
            raise ValueError(f"No provider registered for task: {task}")

        return provider

    def get_supported_tasks(self):

        return list(self.providers.keys())
