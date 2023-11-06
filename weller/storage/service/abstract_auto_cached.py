

import asyncio
from typing import Any, Callable, Iterable
from abc import ABC, abstractmethod
from datetime import datetime

from fast_depends import inject

from weller.types.cache_data import CallableCacheData, CallableCacheServiceData
from weller.storage.service.abstract import AbstractLazyCached


class AbstractLazyAutoCached(AbstractLazyCached, ABC):
    @abstractmethod
    def _get_default_arguments(self) -> dict[str, Any]:
        pass

    def _get_common_arguments(self, **fun_data: Any) -> dict[str, Any]:
        args = self._get_default_arguments()

        return {**args, **fun_data}

    async def set(
            self,
            key: Any,
            duration: float,
            fun: Callable[..., Any],
            value: Any = ...,
            **kwargs
    ):

        """
        This method puts some data in a cache storage and call function while
        :param fun: The function will call when value will become overdue
        :param key: Value's index
        :param value: Some dispather value, if not specified, it is taken from the function
        :param duration: Value's cache time
        :param kwargs: The values that will passed to function
        :return: nothing
        """

        args = kwargs

        if value is Ellipsis:
            args = self._get_common_arguments(**kwargs, key=key, duration=duration)

            fun = inject(fun)

            value = await fun(**args)

        data = CallableCacheData(
            value=value,
            duration=duration,
            fun=fun,
            fun_data=args
        )

        await self._set(key=key, data=data)

    async def _set(self, key: Any, data: CallableCacheData):
        data = CallableCacheServiceData(
            value=data.value,
            set_time=datetime.now(),
            duration=data.duration,
            fun=data.fun,
            fun_data=data.fun_data
        )

        await self._add_data_to_storage(key=key, data=data)

    @abstractmethod
    async def _add_data_to_storage(
            self,
            key: Any,
            data: CallableCacheServiceData
    ):
        pass

    @abstractmethod
    async def _get_data_from_storage(self, key: Any) -> CallableCacheServiceData:
        pass

    async def _update_if_overdue(self, key: str) -> Any:
        """
        Check that data is overdue and update if true
        :param key: data's key
        :return: A old value if not overdue else a new value
        """

        data = await self._get_data_from_storage(key=key)

        if not self._get_data_is_overdue(data):
            return data.value

        if data.bloked:
            return data.value

        data = CallableCacheData(
            value=data.value,
            duration=data.duration,
            fun=data.fun,
            fun_data=data.fun_data,
            bloked=True
        )

        await self._set(
            key=key,
            data=data
        )

        args = self._get_common_arguments(**data.fun_data)
        value = await data.fun(**args)

        data.bloked = False
        data.value = value

        await self._set(
            key=key,
            data=data
        )

        return value

    async def _get(self, key: Any) -> Any:
        """
        This method get value from storage and check that time not expired.
        If data is overdue, get in again
        :param key: Value's index
        :return:
        """

        return await self._update_if_overdue(key)


class AbstractStrictAutoCached(AbstractLazyAutoCached, ABC):
    @abstractmethod
    async def _get_all_keys(self) -> Iterable[Any]:
        pass

    async def _update_all_if_overdue(self, *except_keys: str):
        keys = await self._get_all_keys()
        list_keys = [*keys]

        for key in except_keys:
            list_keys.remove(key)

        for item_key in list_keys:
            updater = self._update_if_overdue(item_key)

            asyncio.create_task(updater)

    async def _get(self, key: Any) -> Any:
        task = asyncio.create_task(self._update_if_overdue(key))

        await self._update_all_if_overdue(key)

        return await task

    async def refresh(self, *except_keys: str):
        """
        This Refresh all overdue values
        :return:
        :param except_keys: refresh except this values
        """

        await self._update_all_if_overdue(*except_keys)
