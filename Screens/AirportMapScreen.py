from Screens.skeletScreenClass import *


class AirportMapScreen(SceletScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Window.bind(mouse_pos=self.on_mouse_move)
        self.overlay = {}
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def _setup_ui(self):
        self._setup_background()
        # Включение возможности прокрутки и масштабирования
        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True, bar_width=10)
        
        # Создание FloatLayout как контейнера для изображения карты с возможностью масштабирования
        self.float_layout = FloatLayout(size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
        
        # Область интереса (например, [x, y, width, height])
        # self.roi = [395, 1000, 40, 60]  # Задайте координаты в соответствии с вашим изображением
        self.all_points = [[395, 1000, 40, 60], [500, 1000, 40, 60]]
        
        # Добавление изображения карты с возможностью масштабирования и свободного позиционирования
        self.map_image = Image(source='images\\b3.webp', allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
        self.float_layout.add_widget(self.map_image)

        self.scroll_view.add_widget(self.float_layout)
        self.add_widget(self.scroll_view)
        
    
    def update(self, dt):
        if len(self.overlay) == 2:
            self.float_layout.remove_widget(self.map_image)
            self.map_image = Image(source='images\\test.jpg', allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
            self.float_layout.add_widget(self.map_image)
        if len(self.overlay) >= 1:
            to_del = self.overlay.copy()
            for i in to_del:
                if len(to_del) >= 1:
                    self.remove_highlighted_point(i, i[-1])
                    self.draw_red_circle(i, i[-1])
        
    
    def on_touch_down(self, touch):
        scroll_x = self.scroll_view.scroll_x * (self.float_layout.width - self.scroll_view.width)
        scroll_y = self.scroll_view.scroll_y * (self.float_layout.height - self.scroll_view.height)
        # Обработка нажатия в определенной области
        x, y = touch.pos[0] + scroll_x - self.float_layout.x, touch.pos[1] + scroll_y - self.float_layout.y
        print(x,)
        print(x, y)
        for roi in self.all_points:
            if roi[0] <= x <= roi[0] + roi[2] and roi[1] <= y <= roi[1] + roi[3]:
                # print("Нажатие внутри ROI")
                popup_content = BoxLayout(orientation='vertical',
                                          spacing=10,
                                          padding=10,
                                          size_hint=(None, None),
                                          size=(200, 150))
                popup = Popup(title='Выбор действия',
                              content=popup_content,
                              size_hint=(None, None), size=(225, 200))
                button1 = Button(text='Отсюда')
                button2 = Button(text='Сюда')
                button3 = Button(text='Отменить выделение')
                popup.content.add_widget(button1)
                popup.content.add_widget(button2)
                popup.content.add_widget(button3)
                button1.bind(on_press=lambda btn: self.handle_button_click('Отсюда', roi,  (1, 0, 0, 1), popup))
                button2.bind(on_press=lambda btn: self.handle_button_click('Сюда', roi, (0, 1, 0, 1), popup))
                button3.bind(on_press=lambda btn: self.handle_button_click('Отменить выделение', roi, (), popup))
                popup.open()
                break  # Stop iterating once found the ROI
        return super(AirportMapScreen, self).on_touch_down(touch)

    def handle_button_click(self, action, roi, color, popup):
        if action == 'Отсюда':
            self.point_1(roi, color)
        elif action == 'Отменить выделение':
            self.remove_all_highlighted_point()
        else:
            self.point_2(roi, color)
        print(f'Вы выбрали действие: {action}')
        popup.dismiss()

    def point_1(self, roi, color):
        if len(self.overlay) == 0:
            self.draw_red_circle(roi, color)

    def point_2(self, roi, color):
        if len(self.overlay) == 1:
            self.draw_red_circle(roi, color)
    
    def draw_red_circle(self, roi, color):
        scroll_x = self.scroll_view.scroll_x * (self.float_layout.width - self.scroll_view.width)
        scroll_y = self.scroll_view.scroll_y * (self.float_layout.height - self.scroll_view.height)
        with self.canvas:
            Color(*color)  # Красный цвет
            self.overlay[(roi[0], roi[1], color)] = Ellipse(pos=(roi[0] - scroll_x + 10, roi[1] - scroll_y + 15), size=(20, 20))
            
    def remove_highlighted_point(self, roi, color):
        if len(self.overlay) >= 1:
            self.canvas.remove(self.overlay[(roi[0], roi[1], color)])
            del self.overlay[(roi[0], roi[1], color)]
            
    def remove_all_highlighted_point(self):
        to_del = self.overlay.copy()
        for i in to_del:
            self.canvas.remove(self.overlay[i])
            del self.overlay[i]
        self.float_layout.remove_widget(self.map_image)
        self.map_image = Image(source='images\\b3.webp', allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
        self.float_layout.add_widget(self.map_image)
    