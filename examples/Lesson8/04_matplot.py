import numpy
import matplotlib.pyplot as plt

from matplotlib.ticker import NullFormatter  # полезно для шкалы

numpy.random.seed(999999)

# создадим некоторые данные в интервале (0, 1)
y = numpy.random.normal(loc=0.5, scale=0.4, size=1000)
y = y[(y > 0) & (y < 1)]
y.sort()
x = numpy.arange(len(y))

# рисуем с различными шкалами осей
plt.figure(1)

# линейные
plt.subplot(221)
plt.plot(x, y)
plt.yscale('линейная')
plt.title('линейная')
plt.grid(True)


# логарифмические
plt.subplot(222)
plt.plot(x, y)
plt.yscale('лог')
plt.title('лог')
plt.grid(True)


# симметричные логарифмические
plt.subplot(223)
plt.plot(x, y - y.mean())
plt.yscale('симлог', linthreshy=0.01)
plt.title('симлог')
plt.grid(True)

# логинт
plt.subplot(224)
plt.plot(x, y)
plt.yscale('логит')
plt.title('логит')
plt.grid(True)

plt.gca().yaxis.set_minor_formatter(NullFormatter())

plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)

plt.show()
