import asyncio
import time

async def my_func(seconds):
    print(f'Эта задача требует {seconds} секунд для завершения')
    time.sleep(seconds)
    return 'Задача завершена'


some_loop = asyncio.get_event_loop()
try:
    print('Задача выполняется')
    our_task = some_loop.create_task(my_func(3))
    some_loop.run_until_complete(our_task)
finally:
    some_loop.close()

print(f"В результате: {our_task.result()}")
