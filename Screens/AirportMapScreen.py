from Screens.skeletScreenClass import *


class AirportMapScreen(SceletScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_move)
        self.overlay = None

    def _setup_ui(self):
        self._setup_background()
        # Включение возможности прокрутки и масштабирования
        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True, bar_width=10)
        
        # Создание FloatLayout как контейнера для изображения карты с возможностью масштабирования
        self.float_layout = FloatLayout(size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
        
        # Область интереса (например, [x, y, width, height])
        self.roi = [395, 1000, 40, 60]  # Задайте координаты в соответствии с вашим изображением
        
        # Добавление изображения карты с возможностью масштабирования и свободного позиционирования
        map_image = Image(source='images\\b1.webp', allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
        self.float_layout.add_widget(map_image)

        self.scroll_view.add_widget(self.float_layout)
        self.add_widget(self.scroll_view)
            
    def on_mouse_move(self, instance, pos):
        scroll_x = self.scroll_view.scroll_x * (self.float_layout.width - self.scroll_view.width)
        scroll_y = self.scroll_view.scroll_y * (self.float_layout.height - self.scroll_view.height)
    
        if self.collide_point(*pos):
            x, y = pos[0] + scroll_x - self.float_layout.x, pos[1] + scroll_y - self.float_layout.y
            
            if self.roi[0] <= x <= self.roi[0] + self.roi[2] and self.roi[1] <= y <= self.roi[1] + self.roi[3]:
                self.highlight_roi(self.roi[0] - scroll_x, self.roi[1] - scroll_y)
            else:
                self.remove_highlight()

    def highlight_roi(self, x, y):
        if not self.overlay:
            with self.canvas:
                Color(1, 0, 0, 0.5)  # Прозрачный красный цвет
                self.overlay = Rectangle(pos=(x, y), size=(self.roi[2], self.roi[3]))

    def remove_highlight(self):
        if self.overlay:
            self.canvas.remove(self.overlay)
            self.overlay = None
            
    def on_touch_down(self, touch):
        scroll_x = self.scroll_view.scroll_x * (self.float_layout.width - self.scroll_view.width)
        scroll_y = self.scroll_view.scroll_y * (self.float_layout.height - self.scroll_view.height)
        # Обработка нажатия в определенной области
        x, y = touch.pos[0] + scroll_x - self.float_layout.x, touch.pos[1] + scroll_y - self.float_layout.y
        if self.roi[0] <= x <= self.roi[0] + self.roi[2] and self.roi[1] <= y <= self.roi[1] + self.roi[3]:
            print("Нажатие внутри ROI")
        return super(AirportMapScreen, self).on_touch_down(touch)
        
    