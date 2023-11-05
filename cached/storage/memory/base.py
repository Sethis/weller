

from typing import Any

from cached.types.cache_data import CacheServiceData


class BaseMemoryStorage:
    def __init__(self):
        self._storage = dict()

    async def _del_data_from_storage(self, key: Any):
        del self._storage[key]

    async def _get_data_from_storage(self, key: Any) -> CacheServiceData:
        return self._storage[key]

    async def _add_data_to_storage(self, key: Any, data: CacheServiceData):
        self._storage[key] = data


class BaseAutoMemoryStorage(BaseMemoryStorage):
    def __init__(self, **kwargs):
        super().__init__()

        self._arguments = kwargs

    def _get_default_arguments(self) -> dict[str, Any]:
        return self._arguments
