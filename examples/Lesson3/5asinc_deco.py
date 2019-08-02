import timeit
import asyncio

def p(txt):
    print(txt)

def plus1(func):
    async def wrapped():
        await asyncio.sleep(3)
        return await func() + 1
    return wrapped


@plus1
async def oneS():
    await asyncio.sleep(3)
    return 3

loop = asyncio.get_event_loop()

start = timeit.default_timer()
print(loop.run_until_complete(oneS()))
stop = timeit.default_timer()
p(stop - start)


@plus1
@plus1
@plus1
@plus1
async def oneS():
    await asyncio.sleep(3)
    return 3

start = timeit.default_timer()
print(loop.run_until_complete(oneS()))
stop = timeit.default_timer()
p(stop - start)