from CanstomClass.settings import *
from Screens.MainScreen import MainScreen
from Screens.FlightInfoScreen import FlightInfoScreen
from Screens.AirportMapScreen import AirportMapScreen

    
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FlightInfoScreen(name='flight_info'))
        sm.add_widget(AirportMapScreen(name='airport_map'))  # Добавляем новый экран
        return sm


if __name__ == "__main__":
    MyApp().run()
