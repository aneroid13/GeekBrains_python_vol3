def p(txt):
    print(txt)

def plus1(func):
    def wrapped():
        return func() + 1
    return wrapped

@plus1
@plus1
def one():
    return 7

p(one())


@plus1
def one():
    return 1

p(one())


@plus1
@plus1
@plus1
@plus1
def one():
    return 1

p(one())