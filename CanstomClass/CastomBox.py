from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class BackgroundBoxLayout(BoxLayout):
    def __init__(self, background_color=[0.5, 0.5, 1, 1], **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(*background_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg_rect, size=self.update_bg_rect)

    def update_bg_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size