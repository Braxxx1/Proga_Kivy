from Screens.skeletScreenClass import *
from CanstomClass.CastomBox import *
from CanstomClass.CastomLabel import *


class ChooseFloor(SceletScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _setup_ui(self):
        self._setup_background()
        # Использование ScrollView
        content = GridLayout(cols=1, spacing=200)
        content.bind(minimum_height=content.setter('height'))
        button_content = GridLayout(cols=1, spacing=10)
        button_content.bind(minimum_height=content.setter('height'))
        
        self._add_info_section(content, "Выбор этажа:", font_size='18sp', bold=True)
        for i in range(1, 4):
            self._add_first_button(button_content, i)
        self._add_mainScreen_button(button_content)
        content.add_widget(button_content)
        self.add_widget(content)

    def show_airport_map(self, i):
        SceletScreen.ind = int(i.text.split()[0])
        print(SceletScreen.ind)
        SceletScreen.start_air = 0
        self.manager.current = 'airport_map'
        
    def show_mainScreen(self, i):
        self.manager.current = 'flight_info'

    def _add_first_button(self, layout, ind):
        # Создание и добавление кнопки для показа карты в GridLayout
        map_button = Button(text=f"{ind} этаж", size_hint_y=None, height=50, background_color=(0.5, 0.5, 1, 1))
        map_button.bind(on_press=self.show_airport_map)
        map_button.pos_hint = {"center_y": 0.5} 
        layout.add_widget(map_button)

    def _add_mainScreen_button(self, layout):
        map_button = Button(text="Назад", size_hint_y=None, height=50, background_color=(0.5, 0.5, 1, 1))
        map_button.bind(on_press=self.show_mainScreen)
        map_button.pos_hint = {"center_y": 0.5} 
        layout.add_widget(map_button)
        
    def _add_info_section(self, layout, text, font_size='16sp', bold=False):
        label = BackgroundLabel(text=text, size_hint_y=None, height=40, font_size=font_size, bold=bold)
        layout.add_widget(label)
