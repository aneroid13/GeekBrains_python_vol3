import numpy

x = numpy.array( [14, 33, 20, 10] )
y = numpy.arange(4)
res = x + y;
print("x=", x, "\ny=", y, 'summ=', res)

x = numpy.array( [11, 22, 33, 44] )
res = x - y;
print("x=", x, "\ny=", y, 'result=', res)

print("\nx=",x,"\n")
print("x**2=", x**2)

print ("2cos(x)=",2*numpy.cos(x))

print("x>=33", x>=33)
z = numpy.ones((2,3), dtype=int)


z+=5
print("z+=5",z)

z*=3
print("z*=3",z)


print("z=",z,"\nz.min()=",z.min())

print("z.max()=",z.max())

print("z.sum()=",z.sum())

print("z=",z,"\nz.min(axis=1)=",z.min(axis=1))

print("z.max(axis=0)=",z.max(axis=0))

print("z.sum(axis=2)=",z.sum(axis=1))

A = numpy.array( [[1,2],[3,4]] )
B = numpy.array( [[1,2], [2,3]] )

print("A=",A,"\nB=",B,"A*B=",A*B)

print("numpy.dot(A,B)=",numpy.dot(A,B))

print("A.dot(B)=",A.dot(B))

x = numpy.arange(9)
print("x = np.arange(9) = ",x)

print("x[4:8]=",x[4:8])

print("x[::-1] = ", x[::-1])

for i in x:
    print(i)

multi_dim_x = numpy.arange(20).reshape(4,5)
for i in multi_dim_x:
    print(i)

for each_element in multi_dim_x.flat:
    print(each_element)

x = numpy.floor(10*numpy.random.random((5,4)))
print("x=",x,"\nразмеры=", x.shape)

print("перевод в одномерный массив - x.ravel()", x.ravel())
print("смена размерностей:\nx.reshape(2,10)=",x.reshape(2,10))
print("numpy.array.T Возвращает транспонированную матрицу", x.T, x.T.shape)

y = x.copy()
print("y is x=",y is x)
print("y.base is x", y.base is x)
x[0,0] = 12345
print(y)
numpy.random.random.__setattr__



print(numpy.sqrt(x))
print(numpy.cos(y))
print(numpy.sin(x))
