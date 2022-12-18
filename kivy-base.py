import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class HomeWindow(Screen):
    pass

class TrucksWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

# Builder.load_file('home.kv')

kv = Builder.load_file('home.kv')

class MyApp(App):

    def build(self):
        Window.maximize()
        return kv

if __name__ == '__main__':
    MyApp().run()
