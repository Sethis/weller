

import copy
from typing import Any
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from cached.types.cache_data import CacheServiceData, CacheData


class AbstractLazyCached(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    async def set(self, key: Any, value: Any, duration: float):
        """
        This method puts some data in a cache storage for a while
        :param key: Value's index
        :param value: Some cached value
        :param duration: Value's cache time
        :return: nothing
        """

        data = CacheData(value=value, duration=duration)

        await self._set(key=key, data=data)

    async def _set(self, key: Any, data: CacheData):
        """
        This method get current datetime and add data to storage
        :param key: Value's index
        :param data: The data bus
        :return: nothing
        """

        data = CacheServiceData(
            value=data.value,
            set_time=datetime.now(),
            duration=data.duration
        )

        await self._add_data_to_storage(key=key, data=data)

    @abstractmethod
    async def _add_data_to_storage(
            self,
            key: Any,
            data: CacheServiceData
    ):
        pass

    async def get(self, key: Any) -> Any:
        """
        Get some data from a storage by key
        :param key: Value's index
        :return:
        """
        return await self._get(key)

    async def _get(self, key: Any) -> Any:
        """
        This method get value from storage and check that time not expired.
        If data is overdue, raises KeyError
        :param key: Value's index
        :return:
        """

        data = await self._get_data_from_storage(key=key)

        if not self._get_data_is_overdue(data):
            return data.value

        await self._del_data_from_storage(key=key)

        raise KeyError()

    @abstractmethod
    async def _get_data_from_storage(self, key: Any) -> CacheServiceData:
        pass

    @staticmethod
    def _get_data_is_overdue(data: CacheServiceData) -> bool:
        delta = timedelta(seconds=data.duration)

        # True if a data is overdue
        return datetime.now() - data.set_time > delta

    @abstractmethod
    async def _del_data_from_storage(self, key: Any):
        pass


class AbstractStrictCached(AbstractLazyCached, ABC):
    async def _get(self, key: Any) -> Any:
        await self._del_all_overdue_values()

        result = await self._get_data_from_storage(key)

        return result.value

    async def _del_all_overdue_values(self):
        """
        This method deletes all values whose time has expired
        :return:
        """
        datum = await self._get_all_data()
        datum = copy.deepcopy(datum)

        for key, item in datum.items():
            if self._get_data_is_overdue(item):
                await self._del_data_from_storage(key)

    @abstractmethod
    async def _get_all_data(self) -> dict[Any, CacheServiceData]:
        pass
