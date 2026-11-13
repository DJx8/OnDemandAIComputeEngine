import os
import time
import logging
import httpx

from dotenv import load_dotenv
from gradio_client import Client

from providers.base import BaseProvider

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HuggingFaceSpaceProvider(BaseProvider):

    SUPPORTED_TASKS = {"translation"}

    def __init__(self, max_attempts=4, retry_delay=5, request_timeout=180):
        super().__init__("huggingface_space")

        self.space_id = os.getenv(
            "HF_SPACE_ID", "Deejay888/Ondemand-translation-engine"
        )

        self.hf_token = os.getenv("HF_TOKEN")
        self.client = None

        self.max_attempts = max_attempts
        self.retry_delay = retry_delay
        self.request_timeout = request_timeout

    def is_available(self) -> bool:
        return bool(self.space_id)

    def _create_client(self):

        client_args = {
            "verbose": False,
            "httpx_kwargs": {"timeout": self.request_timeout},
        }

        if self.hf_token:
            client_args["token"] = self.hf_token

        logger.info("Connecting to Hugging Face Space: %s", self.space_id)

        return Client(self.space_id, **client_args)

    def _get_client(self):

        if self.client is None:
            self.client = self._create_client()

        return self.client

    def execute(self, task: str, **kwargs):

        if not self.supports(task):
            raise ValueError(f"Unsupported task: {task}")

        direction = kwargs.get("direction")
        text = kwargs.get("text")
        language = kwargs.get("language")

        if not direction or not text or not language:
            raise ValueError("direction, text and language are required.")

        last_error = None

        for attempt in range(1, self.max_attempts + 1):

            try:
                logger.info("Translation attempt %s/%s", attempt, self.max_attempts)

                client = self._get_client()

                result = client.predict(
                    direction, text, language, api_name="/translate"
                )

                logger.info("Translation completed successfully.")

                return result

            except httpx.TimeoutException as error:

                self.client = None

                logger.error(
                    "Hugging Face request timed out after %s seconds.",
                    self.request_timeout,
                )

                raise RuntimeError(
                    f"Hugging Face request timed out. " f"Please try again later."
                ) from error

            except Exception as error:

                last_error = error

                if "ZeroGPU" in str(error) or "quota" in str(error).lower():
                    raise RuntimeError(
                        f"Hugging Face GPU quota issue: {error}"
                    ) from error

                self.client = None

                logger.warning("Hugging Face request failed: %s", error)

                if attempt < self.max_attempts:

                    delay = self.retry_delay * attempt

                    logger.info("Retrying in %s seconds...", delay)

                    time.sleep(delay)

        raise RuntimeError(
            f"Hugging Face Space failed after "
            f"{self.max_attempts} attempts. "
            f"Last error: {last_error}"
        ) from last_error
