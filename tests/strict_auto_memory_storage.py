

import asyncio
from typing import Any
from datetime import datetime, timedelta
from dataclasses import dataclass

import pytest

from cached.storage.memory import StrictAutoCachedMemoryStorage


pytestmark = pytest.mark.asyncio

SOME_STR_KEY = "some_key"
SOME_STR_VALUE = "some_value"

SOME_INT_KEY = 123
SOME_INT_VALUE = 321


async def get_some_value_with_01_delay(_data: dict[str, Any]) -> int:
    await asyncio.sleep(0.1)

    return SOME_INT_VALUE


async def get_some_value_with_03_delay(_data: dict[str, Any]) -> int:
    await asyncio.sleep(0.3)

    return SOME_INT_VALUE


async def get_some_value_with_2_delay(_data: dict[str, Any]) -> str:
    await asyncio.sleep(2)

    return SOME_STR_VALUE


async def get_values_from_args(some_key: int) -> SOME_INT_VALUE:
    return some_key


@dataclass
class SomeDataclass:
    str_value: str
    int_value: int


async def test_init_storage():
    assert StrictAutoCachedMemoryStorage()


async def test_add_without_value():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(
        SOME_STR_KEY,
        fun=get_some_value_with_01_delay,
        duration=1
    )

    assert await storage.get(SOME_STR_KEY)


async def test_add_with_value():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(
        SOME_STR_KEY,
        fun=get_some_value_with_2_delay,
        duration=1,
        value=SOME_STR_VALUE
    )

    assert await storage.get(SOME_STR_KEY)


async def test_replace_value():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(
        SOME_STR_KEY,
        fun=get_some_value_with_01_delay,
        duration=1
    )

    await storage.set(
        SOME_STR_KEY,
        fun=get_some_value_with_2_delay,
        duration=1,
        value=SOME_STR_VALUE
    )

    assert await storage.get(SOME_STR_KEY) == SOME_STR_VALUE


async def test_get_str_value():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(
        SOME_INT_KEY,
        duration=1,
        fun=get_some_value_with_01_delay,
        value=SOME_STR_VALUE
    )

    assert await storage.get(SOME_INT_KEY) == SOME_STR_VALUE


async def test_get_without_value():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(
        SOME_INT_KEY,
        duration=1,
        fun=get_some_value_with_01_delay,
    )

    assert await storage.get(SOME_INT_KEY) == SOME_INT_VALUE


async def test_get_class_value():
    storage = StrictAutoCachedMemoryStorage()

    class_ = SomeDataclass(str_value=SOME_STR_VALUE, int_value=SOME_INT_VALUE)

    async def fn(_data: dict[str, Any]):
        return class_

    await storage.set(
        SOME_STR_KEY,
        duration=2,
        fun=fn
    )

    assert await storage.get(SOME_STR_KEY) == class_


async def test_data_is_overdue():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(
        SOME_STR_KEY,
        duration=0.1,
        fun=get_some_value_with_01_delay,
        value="broken_data"
    )

    assert await storage.get(SOME_STR_KEY) == "broken_data"

    await asyncio.sleep(0.1)

    assert await storage.get(SOME_STR_KEY) == SOME_INT_VALUE


async def test_data_is_not_overdue():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(SOME_STR_KEY, fun=get_some_value_with_2_delay, duration=1, value=SOME_STR_VALUE)

    assert await storage.get(SOME_STR_KEY) == SOME_STR_VALUE

    await asyncio.sleep(0.10)

    assert await storage.get(SOME_STR_KEY) == SOME_STR_VALUE


async def test_second_get_override_data():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(SOME_INT_KEY, duration=1, fun=get_some_value_with_2_delay, value="broken_data")

    assert await storage.get(SOME_INT_KEY) == "broken_data"

    await storage.set(SOME_INT_KEY, duration=1, fun=get_some_value_with_01_delay, value=SOME_STR_VALUE)

    assert await storage.get(SOME_INT_KEY) == SOME_STR_VALUE

    await storage.set(SOME_INT_KEY, duration=1, fun=get_some_value_with_01_delay)

    assert await storage.get(SOME_INT_KEY) == SOME_INT_VALUE


async def test_get_full_refresh():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(SOME_INT_KEY, duration=0.5, fun=get_some_value_with_01_delay, value="broken_data")
    await storage.set(SOME_STR_KEY, duration=0.2, fun=get_some_value_with_01_delay, value="broken_data")

    await asyncio.sleep(0.6)

    assert await storage.get(SOME_STR_KEY) == SOME_INT_VALUE

    await asyncio.sleep(0.2)

    start = datetime.now()
    assert await storage.get(SOME_INT_KEY) == SOME_INT_VALUE
    end = datetime.now()

    assert end - start < timedelta(seconds=0.1)


async def test_default_arguments():
    storage = StrictAutoCachedMemoryStorage(some_key=SOME_INT_VALUE)

    await storage.set(key=SOME_STR_KEY, duration=1, fun=get_values_from_args)

    assert await storage.get(key=SOME_STR_KEY) == SOME_INT_VALUE


async def test_fun_arguments():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(key=SOME_STR_KEY, duration=1, fun=get_values_from_args, some_key=SOME_INT_VALUE)

    assert await storage.get(key=SOME_STR_KEY) == SOME_INT_VALUE


async def test_block_by_fun():
    storage = StrictAutoCachedMemoryStorage()

    await storage.set(
        key=SOME_STR_KEY,
        duration=0.1,
        fun=get_some_value_with_01_delay,
        value=SOME_STR_VALUE
    )

    action_1 = storage.get(SOME_STR_KEY)
    action_2 = storage.get(SOME_STR_KEY)
    action_3 = storage.get(SOME_STR_KEY)

    await asyncio.sleep(0.1)

    result = await asyncio.gather(action_1, action_2, action_3)

    print(result[0], result[1], result[2])

    return result[0] != result[1] and result[1] == result[2]
