''' 1 ПРИМЕР
import matplotlib.pyplot as plot
plot.plot([1,2,3,4])
plot.ylabel('Прямая')

plot.plot([1,2,3,4], [0,3,6,9], "ro" )

plot.show()
'''

''' 2 ПРИМЕР
import numpy
import matplotlib.pyplot as plot
arr = numpy.arange(0.0, 9., 0.4)
plot.plot(arr, arr, 'r--', arr, arr**2, 'bs', arr, arr**3, 'g^')

plot.show()
'''

''' 3 ПРИМЕР 
import matplotlib.pyplot as plot
import numpy
numpy.random.seed(99999999)

mu, sigma = 99, 21
x = mu + sigma * numpy.random.randn(10000)

n, bins, patches = plot.hist(x, 50, normed=1, facecolor='g', alpha=0.75)

plot.xlabel('Умы')
plot.ylabel('Вероятность')
plot.title('Историческая диаграмма IQ')
plot.text(60, .025, r'$\mu=100,\ \sigma=15$')
plot.axis([40, 160, 0, 0.03])
plot.grid(True)
plot.show()
'''


'''
import matplotlib.pyplot as plot
import numpy

ax = plot.subplot(111)

t = numpy.arange(0.0, 5.0, 0.01)
s = numpy.cos(2*numpy.pi*t)
line, = plot.plot(t, s, lw=2)

plot.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

plot.ylim(-2,2)
plot.show()
'''
