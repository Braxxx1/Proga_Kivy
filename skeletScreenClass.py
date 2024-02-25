from settings import *


class SceletScreen(Screen):
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


