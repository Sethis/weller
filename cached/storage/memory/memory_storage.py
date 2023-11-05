

from typing import Any, Iterable

from cached.storage.service import (
    AbstractLazyCached,
    AbstractStrictCached,
    AbstractLazyAutoCached,
    AbstractStrictAutoCached
)

from cached.types.cache_data import CacheServiceData
from cached.storage.memory.base import BaseMemoryStorage, BaseAutoMemoryStorage


class LazyCachedMemoryStorage(BaseMemoryStorage, AbstractLazyCached):
    pass


class StrictCachedMemoryStorage(BaseMemoryStorage, AbstractStrictCached):
    async def _get_all_data(self) -> dict[Any, CacheServiceData]:
        return self._storage


class LazyAutoCachedMemoryStorage(BaseAutoMemoryStorage, AbstractLazyAutoCached):
    pass


class StrictAutoCachedMemoryStorage(BaseAutoMemoryStorage, AbstractStrictAutoCached):
    async def _get_all_keys(self) -> Iterable[Any]:
        return self._storage.keys()
