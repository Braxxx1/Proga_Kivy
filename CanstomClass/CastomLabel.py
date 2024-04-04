from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class BackgroundLabel(Label):
    def __init__(self, background_color=[0.39, 0.39, 0.95, 1], **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(*background_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

    def update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
