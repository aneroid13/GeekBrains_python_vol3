import numpy
new_array = numpy.array([5, 6, 7])
print("new_array={}, type={}".format(new_array, type(new_array)))

new_array =  numpy.arange(16).reshape(4,4)
print("массив new_array=\n", new_array)


print("размеры массива:\n", new_array.ndim)

print("имя типа элементов и размер в байтах:", new_array.dtype.name, new_array.size)

other_array = numpy.array([(3.1,5,8), (6.7, 9)])
print (other_array)

other_array = numpy.array([(3.1,5,8), (6.7, 9, 10)], dtype=float)
print ("указываем тип float", other_array)

other_array = numpy.zeros((5,6,3))
print ("пустой массив:",other_array)
