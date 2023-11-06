

import asyncio
from typing import Any
from dataclasses import dataclass

import pytest

from weller.storage.memory import LazyAutoCachedMemoryStorage


pytestmark = pytest.mark.asyncio

SOME_STR_KEY = "some_key"
SOME_STR_VALUE = "some_value"

SOME_INT_KEY = 123
SOME_INT_VALUE = 321


async def long_get_data() -> int:
    await asyncio.sleep(1)

    return 123


