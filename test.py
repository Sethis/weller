

weller = ...

some_db = ...

some_result = ...


@weller.new("sgk", delay=100)
async def update_sgk(db: some_db, other: int) -> some_result:
    some_code = await db.call(other)

    return some_code


@weller.new("pgk", delay=15)
async def update_pgk(db: some_db, other: int) -> some_result:
    some_code = await db.call(other)

    return some_code


@weller.new("sgkstd", delay=10)
async def update_sgkstd(db: some_db, other: int) -> some_result:
    some_code = await db.call(other)

    return some_code


async def get_cacher():
    cacher = await weller.go()

    return cacher
