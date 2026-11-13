from pydantic import BaseModel, Field
from typing import Literal


class TranslationParameters(BaseModel):

    direction: Literal["English → Indian Language", "Indian Language → English"]

    text: str = Field(min_length=1, max_length=5000)

    language: Literal["Hindi", "Malayalam", "Tamil", "Kannada", "Telugu", "Bengali"]

    class Config:
        str_strip_whitespace = True
