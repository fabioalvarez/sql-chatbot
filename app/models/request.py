from pydantic import BaseModel, conint
from typing import Optional


class Request(BaseModel):
    """A model representing an HTTP request."""
    question: str
    retry: Optional[conint(ge=1)] = 1