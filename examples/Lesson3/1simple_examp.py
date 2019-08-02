import asyncio
import time
'''
def func1():
    print('hello')
    #time.sleep(5)

def func2():
    print('hello2')

func1();
func2();
'''

async def func1():
    print('Начинаем function 1')
    await asyncio.sleep(3)
    print('function 1 снова')

async def func2():
    print('Начинаем function 2')
    await asyncio.sleep(3)
    print('function 2 снова')

z1 = asyncio.get_event_loop()
z2 = [z1.create_task(func1()), z1.create_task(func2())]

z3 = asyncio.wait(z2)
z1.run_until_complete(z3)
z1.close()
