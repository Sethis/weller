

import asyncio
from typing import Any, Annotated

from weller import Weller, Depends
from weller.dispather.storage import WellerMemoryStorage


storage = WellerMemoryStorage()


# If first_long = True, then first get of data will download all the data. Default False
weller = Weller(storage=storage, first_long=False)


async def get_db() -> dict[str, Any]:
    return {"some_key": "some_data"}


@weller.add("some_long", duration=5)
async def get_long_data(db: Annotated[dict, Depends(get_db)]):
    await asyncio.sleep(2)

    return db.get("some_key")


async def main():
    await weller.get("some_long")  # it will take 2 seconds
    await weller.get("some_long")  # but it will be done instantly


asyncio.run(main())
