from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Line


class Notification(BoxLayout):
    def __init__(self, **kwargs):
        super(Notification, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.notification_label = Label(text='', size_hint_y=None, height=40)
        self.add_widget(self.notification_label)

    def update_line(self, *args):
        self.line.rectangle = (self.x + 10, self.y + 8, self.width - 15, self.height // 4)

    def show_notification(self, message, duration=5):
        with self.canvas.before:
            Color(0.39, 0.39, 0.95, 1)  # Цвет рамки
            self.line = Line(rectangle=(self.x + 10, self.y - 10, self.width - 15, self.height // 4), width=2)

        self.bind(pos=self.update_line, size=self.update_line)
        self.notification_label.text = message
        Clock.schedule_once(self.clear_notification, duration)

    def clear_notification(self, dt):
        self.notification_label.text = ''
        self.canvas.before.remove(self.line)