

import time
from dataclasses import dataclass

import pytest

from weller.storage.memory import StrictCachedMemoryStorage


pytestmark = pytest.mark.asyncio

SOME_STR_KEY = "some_key"
SOME_STR_VALUE = "some_value"

SOME_INT_KEY = 123
SOME_INT_VALUE = 321


@dataclass
class SomeDataclass:
    str_value: str
    int_value: int


async def test_init_storage():
    assert StrictCachedMemoryStorage()


async def test_add_data_to_storage_with_int_delay():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_STR_KEY, SOME_STR_VALUE, 1)

    assert await storage.get(SOME_STR_KEY)


async def test_add_data_to_storage_with_float_delay():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_STR_KEY, SOME_STR_VALUE, 1.1)

    assert await storage.get(SOME_STR_KEY)


async def test_add_int_data_to_storage():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_INT_KEY, SOME_INT_VALUE, 1.1111)

    assert await storage.get(SOME_INT_KEY)


async def test_replace_value():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_INT_KEY, SOME_INT_VALUE, 1.1111)
    await storage.set(SOME_INT_KEY, SOME_STR_VALUE, 2)

    assert await storage.get(SOME_INT_KEY) == SOME_STR_VALUE


async def test_get_str_value():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_INT_KEY, SOME_STR_VALUE, 1)

    assert await storage.get(SOME_INT_KEY) == SOME_STR_VALUE


async def test_get_int_value():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_INT_KEY, SOME_INT_VALUE, 1)

    assert await storage.get(SOME_INT_KEY) == SOME_INT_VALUE


async def test_get_class_value():
    storage = StrictCachedMemoryStorage()

    class_ = SomeDataclass(str_value=SOME_STR_VALUE, int_value=SOME_INT_VALUE)

    await storage.set(SOME_STR_KEY, class_, 1)

    assert await storage.get(SOME_STR_KEY) == class_


async def test_data_is_overdue():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_STR_KEY, SOME_STR_VALUE, 0.3)

    assert await storage.get(SOME_STR_KEY)

    time.sleep(0.30)

    try:
        await storage.get(SOME_STR_KEY)
        assert False

    except KeyError:
        assert True


async def test_data_is_not_overdue():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_STR_KEY, SOME_STR_VALUE, 0.3)

    assert storage.get(SOME_STR_KEY)

    time.sleep(0.2)

    try:
        await storage.get(SOME_STR_KEY)
        assert True

    except KeyError:
        assert False


async def test_second_get_override_data():
    storage = StrictCachedMemoryStorage()

    await storage.set(SOME_STR_KEY, SOME_STR_VALUE, 0.3)

    assert await storage.get(SOME_STR_KEY)

    time.sleep(0.30)

    try:
        await storage.get(SOME_STR_KEY)
        assert False

    except KeyError:
        pass

    try:
        await storage.get(SOME_STR_KEY)
        assert False

    except KeyError:
        assert True
