'''
В Python есть оператор yield: он действует аналогично return, но возвращает не значение, а объект генератора. Чтобы понять роль yield, разберемся с итераторами и генераторами.
Execution of Coroutine

Execution of coroutine is similar to the generator. When we call coroutine nothing happens, it runs only in response to the next() and send() method. This can be seen clearly in above example, as only after calling __next__() method, out coroutine starts executing. After this call, execution advances to the first yield expression, now execution pauses and wait for value to be sent to corou object. When first value is sent to it, it checks for prefix and print name if prefix present. After printing name it goes through loop until it encounters name = (yield) expression again.

Closing a Coroutine
Coroutine might run indefinitely, to close coroutine close() method is used. When coroutine is closed it generates GeneratorExit exception which can be catched in usual way. After closing coroutine, if we try to send values, it will raise StopIteration exception. Following is a simple example :
'''

def func1(var1): 
    print(f"Searching {var1}")
    try :  
        while True: 
                name = (yield) 
                if var1 in name: 
                    print(name) 
    except GeneratorExit: 
            print("Close coroutine!!!") 
  
z1 = func1("Dear") 
z1.__next__() 
z1.send("Evgeniy") 
z1.send("Dear Sergey") 
z1.send("Atul") 
z1.send("Dear Atul") 
z1.close() 
