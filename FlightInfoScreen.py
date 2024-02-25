from skeletScreenClass import *


class FlightInfoScreen(SceletScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _setup_ui(self):
        self._setup_background()
        # Использование ScrollView
        scroll_view = ScrollView(do_scroll_x=False)
        content = GridLayout(cols=1, spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Добавление заголовков и информации с использованием стилей
        self._add_info_section(content, "Информация о рейсе:", font_size='18sp', bold=True)
        self._add_info_row(content, "Время отправления:", "14:00")
        self._add_info_row(content, "Номер выхода:", "24")
        self._add_info_row(content, "Номер места:", "12A")
        self._add_info_row(content, "Номер и название рейса:", "SU1234, Аэрофлот")
        self._add_info_row(content, "Точка отправления:", "Москва")
        self._add_info_row(content, "Точка прибытия:", "Санкт-Петербург")

        self._add_info_section(content, "Сведения о пассажире:", font_size='18sp', bold=True)
        self._add_info_row(content, "ФИО:", "Иванов Иван Иванович")
        self._add_info_row(content, "Паспортные данные:", "1234 567890")

        self._add_map_button(content)
        
        scroll_view.add_widget(content)
        self.add_widget(scroll_view)

    def _add_info_section(self, layout, text, **text_props):
        # Добавление заголовка секции
        label = Label(text=text, size_hint_y=None, height=40, **text_props)
        layout.add_widget(label)

    def _add_info_row(self, layout, label_text, value_text):
        # Создание строки с информацией
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
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
