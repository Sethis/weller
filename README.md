# Weller

### Installation:
`pip install weller`

### What is it?
weller it's a modern library for caching. It add a TTL cache per item, auto values refresh and also so
easy interface for ruling this

### What it includes:
- Weller - a automatic dispatcher for your perfect cache
- StrictCached and LazyCached - a simply TTL cache per item
- StrictAutoCached and LazyAutoCached - the same as the upper one, but with automatic values refresh 

### Strict and Lazy difference
This library has the concept of strict and lazy caches.

- First, the Lazy, deletes or refreshes only the data that you receive
- Second, the Strict, deletes or refreshes all data from a storage per any request

### Usage examples:

```python
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

```
You can see other examples in weller -> examples  

### Documentation: 
_In development and will be available soon_

### Roadmap:
- Add redis storage
- Work and work with stability and security
