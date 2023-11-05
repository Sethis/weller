

from typing import Any, Callable, Coroutine
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CacheData:
    value: Any
    delay: float


@dataclass
class CallableCacheData(CacheData):
    fun: Callable[[dict[str, Any]], Coroutine[Any, Any, Any]]
    fun_data: dict[str, Any]
    bloked: bool = False


@dataclass
class CacheServiceData(CacheData):
    set_time: datetime


@dataclass
class CallableCacheServiceData(CallableCacheData, CacheServiceData):
    pass
