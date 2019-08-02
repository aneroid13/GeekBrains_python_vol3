import random

import kivy  
from kivy.app import App  
from kivy.uix.widget import Widget 
from kivy.graphics import Rectangle, Color 
from kivy.clock import Clock
kivy.require("1.9.1")  

class CanvasWidget(Widget): 

    def __init__(self, **kwargs): 

        super(CanvasWidget, self).__init__(**kwargs) 
  
        with self.canvas: 
            Color(1, 1, 1, 1)
  
            self.rect = Rectangle(pos=(10, 10), size=(40, 40))
            self.rect2 = Rectangle(pos=(20, 20), size=(40, 40))
  
            self.bind(pos = self.update_rect, size = self.update_rect) 
  
    def update_rect(self, *args): 
        x1, y1 = random.randint(1,1000), random.randint(1,1000)
        x2, y2 = random.randint(1,1000), random.randint(1,1000)
        self.rect.pos = (x1, y1)
        self.rect2.pos = (x2, y2)
  
class CanvasApp(App): 
    def build(self): 
        game = CanvasWidget()
        Clock.schedule_interval(game.update_rect, 1.0 / 2.0)
        return game
  
CanvasApp().run() 
