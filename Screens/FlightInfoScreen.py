from Screens.skeletScreenClass import *
from CanstomClass.CastomBox import *
from CanstomClass.CastomLabel import *
import json
from BD import get_info


class FlightInfoScreen(SceletScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _setup_ui(self):
        self._setup_background()
        # Использование ScrollView
        scroll_view = ScrollView(do_scroll_x=False)
        content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        data = get_info_about_boarding_pass("1111111111")
        data = data[data["num_boarding"]]
        # Добавление заголовков и информации с использованием стилей
        self._add_info_section(content, "Информация о рейсе:", font_size='18sp', bold=True)
        self._add_info_row(content, f"Время отправления:", data['time_from'])
        self._add_info_row(content, "Номер выхода:", data["gate"])
        self._add_info_row(content, "Номер места:", data["num_seat"])
        self._add_info_row(content, "Номер рейса:", data["num_flight"])
        self._add_info_row(content, "Точка отправления:", data["name_city_from"])
        self._add_info_row(content, "Точка прибытия:", data["name_city_to"])
        
        self._add_info_section(content, "Сведения о пассажире:", font_size='18sp', bold=True)
        self._add_info_row(content, "ФИО:", data["surname"] + " " + data["given_names"])
        self._add_info_row(content, "Паспортные данные:", str(data["num_passport"]))

        self._add_map_button(content)
        
        scroll_view.add_widget(content)
        self.add_widget(scroll_view)

    def _add_info_section(self, layout, text, font_size='16sp', bold=False):
        label = BackgroundLabel(text=text, size_hint_y=None, height=40, font_size=font_size, bold=bold)
        layout.add_widget(label)

    def _add_info_row(self, layout, label_text, value_text):
        row = BackgroundBoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        row.add_widget(Label(text=label_text, size_hint_x=0.5))
        row.add_widget(Label(text=value_text, size_hint_x=0.5))
        layout.add_widget(row)
        
    def show_airport_map(self, instance):
        self.manager.current = 'airport_map'

    def _add_map_button(self, layout):
        # Создание и добавление кнопки для показа карты в GridLayout
        map_button = Button(text="Показать карту аэропорта", size_hint_y=None, height=50)
        map_button.bind(on_press=self.show_airport_map)
        layout.add_widget(map_button)
