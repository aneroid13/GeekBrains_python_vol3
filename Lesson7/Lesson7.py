import matplotlib.pyplot as plot
import numpy as np

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


# y=x*2-cos(x)
# y=x^3-sqrt(x)

x = np.arange(0, np.float(10), np.float32(0.1), dtype=float)

y1 = x * 2 - np.cos(x)
y2 = np.power(x, 3) - np.sqrt(x)

plot.figure(1)
plot.subplot(211)
plot.plot(x, y1, 'g')

plot.subplot(212)
plot.plot(x, y2, 'r--')

#plot.show()


class MathApp(App):
    def build(self):
        self.title = 'Math plot'
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plot.gcf()))
        return box


if __name__ == '__main__':
    Builder.load_string(kv)
    MathApp().run()
