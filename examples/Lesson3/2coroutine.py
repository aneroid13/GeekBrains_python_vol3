import asyncio

# definition of a coroutine
async def coroutine_1():
    print('1 1')
    await asyncio.sleep(4)

    print('1 2')

# definition of a coroutine
async def coroutine_2():
    print('2 1')
    await asyncio.sleep(5)

    print('2 2')

# this is the event loop
loop = asyncio.get_event_loop()

# schedule both the coroutines to run on the event loop
loop.run_until_complete(asyncio.gather(coroutine_1(), coroutine_2()))
