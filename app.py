from CanstomClass.settings import *
from Screens.MainScreen import MainScreen
from Screens.FlightInfoScreen import FlightInfoScreen
from Screens.AirportMapScreen import AirportMapScreen
from Screens.ChooseFloor import ChooseFloor

    
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FlightInfoScreen(name='flight_info'))
        sm.add_widget(ChooseFloor(name='choose_floor'))
        sm.add_widget(AirportMapScreen(name='airport_map'))
        return sm


if __name__ == "__main__":
    MyApp().run()
