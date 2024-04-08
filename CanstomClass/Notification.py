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

        self.button_layout = BoxLayout(size_hint_y=None, height=40, padding=[80, 10, 10, 10])
        self.ok_button = Button(text='OK', size_hint_x=None, width=100)
        self.ok_button.bind(on_release=self.on_ok)
        self.ok_button.opacity = 0
        self.cancel_button = Button(text='Отмена', size_hint_x=None, width=100)
        self.cancel_button.bind(on_release=self.on_cancel)
        self.cancel_button.opacity = 0
        self.button_layout.add_widget(self.ok_button)
        self.button_layout.add_widget(self.cancel_button)
        self.add_widget(self.button_layout)

    def update_line(self, *args):
        self.line.rectangle = (self.x + 10, self.y, self.width - 15, self.height // 3)

    def show_notification(self, message, duration=5):
        with self.canvas.before:
            Color(0.39, 0.39, 0.95, 1)  # Цвет рамки
            self.line = Line(rectangle=(self.x + 10, self.y, self.width - 15, self.height // 3), width=2)

        self.bind(pos=self.update_line, size=self.update_line)
        self.notification_label.text = message
        self.ok_button.opacity = 1
        self.cancel_button.opacity = 1
        Clock.schedule_once(self.clear_notification, duration)

    def clear_notification(self, dt):
        self.notification_label.text = ''
        self.ok_button.opacity = 0
        self.cancel_button.opacity = 0
        self.canvas.before.remove(self.line)

    def on_ok(self, instance):
        print("OK нажата")

    def on_cancel(self, instance):
        print("Отмена нажата")