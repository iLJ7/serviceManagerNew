import kivy

kivy.require('2.0.0')

from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class MyApp(App):

    def build(self):
        
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height = layout.setter('height'))
        
        for i in range(100):
            button = Button(text=str(i), size_hint_y=None, height=40)
            
            layout.add_widget(button)
        
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        root.add_widget(layout)

        return root

if __name__ == '__main__':
    MyApp().run() 