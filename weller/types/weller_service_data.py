

from typing import Any, Callable
from pydantic import BaseModel


class FunctionData(BaseModel):
    key: str
    duration: int
    fun:  Callable[..., Any]
    fun_data: dict[str, Any]
