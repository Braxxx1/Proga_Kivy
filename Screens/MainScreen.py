from Screens.skeletScreenClass import *


class MainScreen(SceletScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_scan = False
        Clock.schedule_interval(self.update, 60.0 / 1)

    def _setup_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[10, 50, 10, 50], size_hint=(1, None), height=500)
        self.notif = Notification()
        layout.add_widget(self.notif)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.8}
        
        label = Label(text="Добро пожаловать!", font_size='20sp', size_hint=(1, None), height=50)
        layout.add_widget(label)
        
        self._setup_background()
        
        self.ticket_input = TextInput(hint_text='Введите номер посадочного талона', size_hint=(1, None), height=40, multiline=False)
        layout.add_widget(self.ticket_input)
        
        button_layout = self._create_button_layout()
        layout.add_widget(button_layout)
        
        self.add_widget(layout)

    def update(self, dt):
        if SceletScreen.start_go and self.is_scan:
            data = get_info_about_boarding_pass("1111111111")
            data = data[data["num_boarding"]]['time_from']
            current_datetime = datetime.now()
            # Задайте другую дату времени
            # other_datetime_str = data
<<<<<<< HEAD
            other_datetime_str = "2024-04-9 00:51:00.000"
=======
            other_datetime_str = "2024-04-8 22:30:00.000"
>>>>>>> 7a2c780b958b8d983905443a4f9cf8aff6fff080
            other_datetime = datetime.strptime(other_datetime_str, "%Y-%m-%d %H:%M:%S.%f")

            # Вычислите разницу между датами
            difference = current_datetime - other_datetime

            # Проверьте, что разница составляет 15 минут
            if abs(difference) <= timedelta(minutes=15):
                popup_content = BoxLayout(orientation='vertical',
                                            spacing=10,
                                            padding=10,
                                            size_hint=(None, None),
                                            size=(200, 150))
                self.popup = Popup(title='Пройдите на посадку',
                                content=popup_content,
                                size_hint=(None, None), size=(225, 200))
                button1 = Button(text='Пройти')
                button2 = Button(text='Отмена')
                self.popup.content.add_widget(button1)
                self.popup.content.add_widget(button2)
                button1.bind(on_press=lambda btn: self.go_to_passage()) #self.handle_button_click('Отсюда', roi,  (1, 0, 0, 1), popup))
                button2.bind(on_press=lambda btn: self.cansel())
                self.popup.open()

    def go_to_passage(self):
        SceletScreen.dime_to_go = image_notification("1111111111")
        SceletScreen.ind = SceletScreen.dime_to_go['num_floor']
        self.popup.dismiss()
        self.manager.current = 'airport_map'
        print(1)
        
        
    def cansel(self):
        self.popup.dismiss()
    
    def _create_button_layout(self):
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        scan_button = Button(text="Сканировать штрих-код", background_color=(0.5, 0.5, 1, 1))
        scan_button.bind(on_press=self.scan_barcode)
        button_layout.add_widget(scan_button)
        auth_button = Button(text="Авторизация", background_color=(0.5, 0.5, 1, 1))
        auth_button.bind(on_press=self.authenticate)
        button_layout.add_widget(auth_button)
        return button_layout

    def scan_barcode(self, instance):
        self.notif.show_notification("Вы успешно авторизовались")
        scaning_boarding_pass(3, "1111111111")
        SceletScreen.ticket_input = "1111111111"
        self.ticket_input.text = "1111111111"
        print("Штрих-код был отсканирован")
        self.is_scan = True

    def authenticate(self, instance):
        if self.is_scan:
            print("Пользователь был авторизован")
            self.manager.current = 'flight_info'

