

from typing import Any, Callable
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CacheData:
    value: Any
    duration: float


@dataclass
class CallableCacheData(CacheData):
    fun: Callable[..., Any]
    fun_data: dict[str, Any]
    bloked: bool = False


@dataclass
class CacheServiceData(CacheData):
    set_time: datetime


@dataclass
class CallableCacheServiceData(CallableCacheData, CacheServiceData):
    pass
