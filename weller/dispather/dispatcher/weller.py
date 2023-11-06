

import asyncio
from typing import Callable, Any, Coroutine

from weller.storage.service.abstract_auto_cached import AbstractStrictAutoCached
from weller.types.weller_service_data import FunctionData


class Weller:
    def __init__(
            self,
            storage: AbstractStrictAutoCached,
            first_long: bool = False
    ):
        self._storage: AbstractStrictAutoCached = storage
        self._functions: list[FunctionData] = []
        self._was_started: bool = False
        self._initialization_process: bool = False
        self._first_long: bool = first_long

    def add(self, key: str, duration: int) -> Callable[..., Any]:
        def decorator(func) -> Callable[..., Any]:
            fun_data = {}

            data = FunctionData(
                fun=func,
                duration=duration,
                key=key,
                fun_data=fun_data
            )

            self._functions.append(data)

            return func

        return decorator

    async def _set_all_functions_to_storage(self, *except_key: str):
        self._initialization_process = True

        result: list[Coroutine[Any, Any, Any]] = []

        for func in self._functions:
            if func.key in except_key:
                continue

            setter = self._storage.set(
                key=func.key,
                duration=func.duration,
                fun=func.fun,
                **func.fun_data
            )

            result.append(setter)

        await asyncio.gather(*result)

        self._initialization_process = False

    def _get_function_by_key(self, key: str) -> FunctionData:
        for func in self._functions:
            if func.key == key:
                return func

        raise KeyError

    async def get(self, key: str) -> Any:
        if self._was_started and not self._initialization_process:
            return await self._storage.get(key)

        if not self._initialization_process:
            if self._first_long:
                await self._set_all_functions_to_storage(key)

            else:
                asyncio.create_task(self._set_all_functions_to_storage(key))

        func = self._get_function_by_key(key)

        await self._storage.set(
            key=key,
            duration=func.duration,
            fun=func.fun,
            **func.fun_data
        )

        self._was_started = True

        return await self._storage.get(key)
