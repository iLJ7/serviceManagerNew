import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

Builder.load_file('home.kv')

class MyGridLayout(Widget):
    
    name = ObjectProperty(None)
    pizza = ObjectProperty(None)
    color = ObjectProperty(None)

class MyApp(App):

    def build(self):
        Window.maximize()
        return MyGridLayout()

if __name__ == '__main__':
    MyApp().run()
