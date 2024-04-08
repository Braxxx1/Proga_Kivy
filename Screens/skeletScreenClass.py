from CanstomClass.settings import *


class SceletScreen(Screen):
    ticket_input = ''
    airport_map_start = {0:"",
                         1:'images\\b1.webp',
                         2:'images\\b2.webp',
                         3:'images\\b3.webp'}
    ind = 0
    dime_to_go = ''
    start_go = True
    start_air = 0
    def __init__(self, **kwargs):
        super(SceletScreen, self).__init__(**kwargs)
        self._setup_ui()

    def _setup_background(self):
        with self.canvas.before:
            Color(0.5, 0.5, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


