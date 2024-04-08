from Screens.skeletScreenClass import *


class AirportMapScreen(SceletScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Window.bind(mouse_pos=self.on_mouse_move)
        self.start = 0
        self.overlay = {}
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def _setup_ui(self):
        self._setup_background()
        # Включение возможности прокрутки и масштабирования
        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True, bar_width=10)
        
        # Создание FloatLayout как контейнера для изображения карты с возможностью масштабирования
        self.float_layout = FloatLayout(size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
        
        # Область интереса (например, [x, y, width, height])
        self.all_points = []
        self.ind_points = []
        self.airport_from = ''
        self.map_image = Image(source=SceletScreen.airport_map_start[SceletScreen.ind], allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
        self.float_layout.add_widget(self.map_image)

        self.scroll_view.add_widget(self.float_layout)
        self.add_widget(self.scroll_view)
        
        map_button = Button(text="Назад", size_hint_y=None, height=50, background_color=(0.5, 0.5, 1, 1))
        map_button.bind(on_press=self.show_mainScreen)
        self.add_widget(map_button)
    
    def update(self, dt):
        if self.start == 0 and SceletScreen.ind != 0:
            data = get_info_about_boarding_pass(SceletScreen.ticket_input)
            self.airport_from = data[data["num_boarding"]]["airport_from"]
            get_points = get_points_airport(self.airport_from)
            for i in get_points:
                for j in get_points[i][SceletScreen.ind]:
                    self.ind_points.append(j["id_point"])
                    self.all_points.append((int(j['x']), int(j['y']), int(j['width']), int(j['height'])))
            self.start = 1
            self.float_layout.remove_widget(self.map_image)
            self.map_image = Image(source=SceletScreen.airport_map_start[SceletScreen.ind], allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
            self.float_layout.add_widget(self.map_image)    
        # print(SceletScreen.airport_map_start)
        if len(self.overlay) == 2:
            take_id = []
            for i in self.overlay:
                for j in range(len(self.all_points)):
                    # print(i[:-1], j, i[:-1] in j)
                    if i[0] in self.all_points[j] and i[1] in self.all_points[j]:
                        take_id.append(self.ind_points[j])
            
                # print(i[:-1])
            # print(get_route(take_id[0], take_id[1], 'SVO'))
            self.float_layout.remove_widget(self.map_image)
            self.map_image = Image(source=get_route(take_id[0], take_id[1], self.airport_from), allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
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
            self.overlay[(roi[0], roi[1], color)] = Ellipse(pos=(roi[0] - scroll_x, roi[1] - scroll_y), size=(20, 20))
            
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
        self.map_image = Image(source=SceletScreen.airport_map_start[SceletScreen.ind], allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(Window.width * 2, Window.height * 2))
        self.float_layout.add_widget(self.map_image)
    
    def show_mainScreen(self, i):
        self.start = 0
        SceletScreen.ind = 0
        self.manager.current = 'choose_floor'