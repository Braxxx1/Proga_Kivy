from Screens.skeletScreenClass import *


class MainScreen(SceletScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_scan = False

    def _setup_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[10, 50, 10, 50], size_hint=(1, None), height=500)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.8}
        
        label = Label(text="Добро пожаловать!", font_size='20sp', size_hint=(1, None), height=50)
        layout.add_widget(label)
        
        self._setup_background()
        
        self.ticket_input = TextInput(hint_text='Введите номер посадочного талона', size_hint=(1, None), height=40, multiline=False)
        layout.add_widget(self.ticket_input)
        
        button_layout = self._create_button_layout()
        layout.add_widget(button_layout)
        
        self.add_widget(layout)

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
        self.ticket_input.text = "1111111111"
        print("Штрих-код был отсканирован")
        self.is_scan = True

    def authenticate(self, instance):
        if self.is_scan:
            print("Пользователь был авторизован")
            self.manager.current = 'flight_info'

